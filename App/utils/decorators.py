from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from functools import wraps
from App.utils.auth_utils import verify_google_token

def require_google_auth(endpoint_func):
    @wraps(endpoint_func)
    async def wrapper(request: Request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid token.")

        token = auth_header.split("Bearer ")[1]
        user_info = verify_google_token(token)

        if not user_info:
            raise HTTPException(status_code=401, detail="Invalid or expired token.")

        request.state.user_id = user_info['sub']  # unique ID
        request.state.user_email = user_info.get("email")
        return await endpoint_func(request, *args, **kwargs)
    return wrapper
