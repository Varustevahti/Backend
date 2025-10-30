import os
import httpx
from jose import jwt
from fastapi import Request, HTTPException, status

CLERK_JWKS_URL = os.getenv("CLERK_JWKS_URL")

_jwks_cache: None

async def get_current_user_id(request: Request) -> str:
    auth = request.headers.get("authorization") or request.headers.get("Authorization")
    if not auth or not auth.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    token = auth.split(" ", 1)[1]

    global _jwks_cache
    if _jwks_cache is None:
        async with httpx.AsyncClient(timeout=5) as client:
            responde = await client.get(CLERK_JWKS_URL)
            _jwks_cache = responde.json()
    try:
        headers = jwt.get_unverified_header(token)
        key = next(k for k in _jwks_cache["keys"] if k["kid"] == headers["kid"])
        claims = jwt.decode(token, key, algorithms=[key.get("alg", "RS256")])
        return claims["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
