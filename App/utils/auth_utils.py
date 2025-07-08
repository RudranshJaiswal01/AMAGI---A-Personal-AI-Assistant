# app/utils/auth_utils.py
# import os
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from App.config import GOOGLE_CLIENT_ID

def verify_google_token(token: str):
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            grequests.Request(),
            GOOGLE_CLIENT_ID  # MUST match your frontend client ID
        )
        return idinfo  # includes sub, email, etc.
    except Exception as e:
        print("Token verification failed:", e)
        return None
