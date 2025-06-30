import os, sys, glob, importlib.util, json, requests
from fastapi import FastAPI, Request, Response, HTTPException

PLUGIN_DIR = "./plugins"
class PluginManager:
    def __init__(self, plugin_dir=PLUGIN_DIR):
        self.plugins = []
        sys.path.append(plugin_dir)
        for pyfile in glob.glob(os.path.join(plugin_dir, "*.py")):
            mod_name = os.path.splitext(os.path.basename(pyfile))[0]
            if mod_name.startswith("_"): continue
            spec = importlib.util.spec_from_file_location(mod_name, pyfile)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            self.plugins.append(mod)
    def before_request(self, request, json_body):
        for plugin in self.plugins:
            if hasattr(plugin, "before_request"):
                plugin.before_request(request, json_body)
    def after_response(self, request, response):
        for plugin in self.plugins:
            if hasattr(plugin, "after_response"):
                plugin.after_response(request, response)

plugin_manager = PluginManager()
app = FastAPI(title="GateKeeperMCP Gateway")
BACKEND_API = os.getenv("BACKEND_API", "http://gatekeeper-server:8000")

@app.post("/execute_mcp")
async def execute_mcp(request: Request):
    body = await request.body()
    try:
        json_body = json.loads(body)
    except Exception:
        raise HTTPException(400, "Invalid JSON")
    plugin_manager.before_request(request, json_body)
    headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
    resp = requests.post(f"{BACKEND_API}/execute", data=body, headers=headers)
    plugin_manager.after_response(request, resp)
    return Response(content=resp.content, status_code=resp.status_code, media_type=resp.headers.get("content-type"))

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/openapi.json")
def openapi_spec():
    with open("./schemas/mcp_protocol_openapi.yaml") as f:
        return Response(content=f.read(), media_type="application/yaml")
