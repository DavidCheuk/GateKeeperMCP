import requests
from fastapi import HTTPException
OPA_URL = "http://opa:8181/v1/data/enterprise/policy"
def before_request(request, json_body):
    user = getattr(request.state, "auth_user", None)
    input_obj = {
        "user": user,
        "action": json_body.get("action"),
        "parameters": json_body.get("parameters"),
        "headers": dict(request.headers),
        "metadata": json_body.get("metadata", {}),
    }
    response = requests.post(OPA_URL, json={"input": input_obj})
    result = response.json().get("result", {})
    if not result.get("allow", False):
        msg = result.get("reason", "Enterprise OPA policy denied the request")
        raise HTTPException(403, msg)
