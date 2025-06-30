from fastapi import HTTPException
API_KEYS = {"service1": "sk-abc123", "service2": "sk-def456"}
def before_request(request, json_body):
    key = request.headers.get("x-api-key")
    if not key or key not in API_KEYS.values():
        raise HTTPException(401, "Missing or invalid API key")
    request.state.auth_user = next(k for k, v in API_KEYS.items() if v == key)
