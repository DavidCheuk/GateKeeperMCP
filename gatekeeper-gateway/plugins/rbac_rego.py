import requests
from fastapi import HTTPException
OPA_URL = "http://opa:8181/v1/data/mcp/allow"
def before_request(request, json_body):
    user = getattr(request.state, "auth_user", None)
    action = json_body.get("action")
    input_obj = {"user": user, "action": action}
    response = requests.post(OPA_URL, json={"input": input_obj})
    if not response.json().get("result", False):
        raise HTTPException(403, "Access denied by policy")
