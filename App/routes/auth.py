from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from App.utils.auth_utils import verify_google_token

router = APIRouter()

class TokenInput(BaseModel):
    token: str

@router.post("/auth/verify")
async def verify_token(data: TokenInput, request: Request):
    try:
        payload = verify_google_token(data.token)
        return {"status": "success", "user_id": payload["sub"], "email": payload["email"]}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
