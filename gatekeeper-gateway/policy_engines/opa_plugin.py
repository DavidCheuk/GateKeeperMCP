from unittest import result
import requests
from policy_engines.base import PolicyEnginePlugin

class OPAPlugin(PolicyEnginePlugin):
    def __init__(self, opa_url):
        self.opa_url = opa_url

    def evaluate(self, context: dict, action: str, resource: str, **kwargs) -> dict:
        payload = {
            "input": {
                "user": context.get("user"),
                "action": action,
                "parameters": context.get("parameters"),
                "metadata": context.get("metadata"),
                **kwargs
            }
        }
        try:
            resp = requests.post(self.opa_url, json=payload, timeout=2)
            resp.raise_for_status()
            result = resp.json().get("result", {})
            print(f"OPA Response: {result}", flush=True)

            allow = result.get("allow", False)
            # Only show deny_reason if allow is False
            if allow:
                reason = "Allowed by policy"
            else:
                reason = result.get("deny_reason", "Denied by policy")
            return {"allow": allow, "reason": reason}
        except Exception as ex:
            return {"allow": False, "reason": f"OPA error: {ex}"}
