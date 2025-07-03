import os, sys, glob, importlib.util, json, requests
from fastapi import FastAPI, Request, Response, HTTPException

PLUGIN_DIR = "./plugins"
POLICY_ENGINE_DIR = "./policy_engines"
class PluginManager:
    def __init__(self, plugin_dir=PLUGIN_DIR):
        self.plugins = []
        sys.path.append(plugin_dir)
        sys.path.append(POLICY_ENGINE_DIR)
        for pyfile in glob.glob(os.path.join(plugin_dir, "*.py")):
            mod_name = os.path.splitext(os.path.basename(pyfile))[0]
            if mod_name.startswith("_"): continue
            spec = importlib.util.spec_from_file_location(mod_name, pyfile)
            if spec is None or spec.loader is None:
                print(f"Warning: Could not load plugin spec for {mod_name} at {pyfile}")
                continue
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            self.plugins.append(mod)

    def before_request(self, request, json_body, decision_trace):
        for plugin in self.plugins:
            if hasattr(plugin, "before_request"):
                try:
                    plugin.before_request(request, json_body, decision_trace)
                    decision_trace.append({
                        "plugin": plugin.__name__, "action": "allow", "reason": "Passed checks"
                    })
                except HTTPException as e:
                    decision_trace.append({
                        "plugin": plugin.__name__, "action": "block", "reason": str(e.detail)
                    })
                    raise HTTPException(400, {"error": str(e.detail), "decision_trace": decision_trace})

    def after_response(self, request, response, decision_trace):
        for plugin in self.plugins:
            if hasattr(plugin, "after_response"):
                plugin.after_response(request, response, decision_trace)

# Dynamically load policy engine (e.g., OPA)
def load_policy_engine():
    policy_engines_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'policy_engines'))
    opa_plugin_path = os.path.join(policy_engines_dir, 'opa_plugin.py')

    if not os.path.exists(opa_plugin_path):
        raise ImportError(f"opa_plugin.py not found at {opa_plugin_path}")

    spec = importlib.util.spec_from_file_location("opa_plugin", opa_plugin_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec for opa_plugin.py at {opa_plugin_path}")

    opa_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(opa_module)
    OPAPlugin = opa_module.OPAPlugin

    opa_url = os.getenv("OPA_URL", "http://opa:8181/v1/data/enterprise/policy")
    return OPAPlugin(opa_url)

plugin_manager = PluginManager()
policy_engine = load_policy_engine()
app = FastAPI(title="GateKeeperMCP Gateway")
BACKEND_API = os.getenv("BACKEND_API", "http://gatekeeper-server:8000")

@app.post("/execute_mcp")
async def execute_mcp(request: Request):
    decision_trace = []
    body = await request.body()
    try:
        json_body = json.loads(body)
    except Exception:
        raise HTTPException(400, {"error": "Invalid JSON", "decision_trace": decision_trace})

    # ---- PROMPT SANITIZATION CHAIN ----
    from plugins.prompt_sanitizer_chain import run_prompt_sanitizer_chain
    params = json_body.get("parameters", {})
    if isinstance(params, dict) and "prompt" in params and isinstance(params["prompt"], str):
        try:
            params["prompt"] = run_prompt_sanitizer_chain(params["prompt"])
            decision_trace.append({
                "plugin": "prompt_sanitizer_chain", "action": "allow", "reason": "Sanitization passed"
            })
            json_body["parameters"] = params
        except Exception as e:
            decision_trace.append({
                "plugin": "prompt_sanitizer_chain", "action": "block", "reason": str(e)
            })
            return Response(
                status_code=400,
                content=json.dumps({"detail": str(e), "decision_trace": decision_trace}),
                media_type="application/json"
            )

    # ---- POLICY CHECK ----
    # Insert here before running other plugins, or after (your choice)
    try:
        # Map your API input to OPA as needed
        user = json_body.get("user")
        action = json_body.get("action")
        resource = json_body.get("parameters", {}).get("dataset")
        # Pass full json_body to context if needed
        policy_decision = policy_engine.evaluate(
            context=json_body, action=action, resource=resource
        )
        if not policy_decision.get("allow", False):
            decision_trace.append({
                "plugin": "opa_policy", "action": "block", "reason": policy_decision.get("reason", "Blocked by policy")
            })
            return Response(
                status_code=400,
                content=json.dumps({"detail": policy_decision.get("reason", "Blocked by policy"), "decision_trace": decision_trace}),
                media_type="application/json"
            )
        decision_trace.append({
            "plugin": "opa_policy", "action": "allow", "reason": policy_decision.get("reason", "Allowed by policy")
        })
    except Exception as e:
        decision_trace.append({
            "plugin": "opa_policy", "action": "block", "reason": str(e)
        })
        return Response(
            status_code=400,
            content=json.dumps({"detail": str(e), "decision_trace": decision_trace}),
            media_type="application/json"
        )

    # ---- PLUGIN CHAIN ----
    try:
        plugin_manager.before_request(request, json_body, decision_trace)
    except HTTPException as e:
        # e.detail may now include the trace
        return Response(
            status_code=400,
            content=json.dumps({"detail": getattr(e, "detail", str(e)), "decision_trace": decision_trace}),
            media_type="application/json"
        )

    headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
    resp = requests.post(f"{BACKEND_API}/execute", data=body, headers=headers)
    plugin_manager.after_response(request, resp, decision_trace)

    return Response(
        content=json.dumps({
            "status": "executed",
            "echo": json_body,
            "decision_trace": decision_trace
        }),
        status_code=resp.status_code,
        media_type="application/json"
    )

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/openapi.json")
def openapi_spec():
    with open("./schemas/mcp_protocol_openapi.yaml") as f:
        return Response(content=f.read(), media_type="application/yaml")
