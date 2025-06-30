from jose import jwt, JWTError
import requests
from fastapi import HTTPException
OIDC_ISSUER = "https://issuer.example.com/.well-known/openid-configuration"
OIDC_AUDIENCE = "gatekeeper-gateway"
_jwks = None
def _get_jwks():
    global _jwks
    if not _jwks:
        conf = requests.get(OIDC_ISSUER).json()
        jwks_uri = conf.get("jwks_uri")
        _jwks = requests.get(jwks_uri).json()
    return _jwks
def before_request(request, json_body):
    authz = request.headers.get("authorization", "")
    if not authz.lower().startswith("bearer "):
        return
    token = authz[7:]
    jwks = _get_jwks()
    try:
        claims = jwt.decode(token, jwks, algorithms=["RS256"], audience=OIDC_AUDIENCE)
        request.state.auth_user = claims.get("sub")
        request.state.auth_roles = claims.get("roles", [])
    except JWTError as e:
        raise HTTPException(401, f"Invalid JWT: {e}")
