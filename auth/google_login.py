import json
from google_auth_oauthlib.flow import InstalledAppFlow
import requests

from config import host, port

# Load your client_secret.json from Google Developer Console
def google_login():
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret_206770168103-vcgubvapv26qctc6tobta4buth93hjvl.apps.googleusercontent.com.json',  # You must have this downloaded
        scopes=["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]
    )
    creds = flow.run_local_server(port=0)
    
    # Get the ID token to send to the backend
    id_token = creds.id_token
    print("ID Token:", id_token)

    # Send it to your backend
    headers = {"Authorization": f"Bearer {id_token}"}
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        "http://127.0.0.1:8000/auth/verify",
        json={"token": id_token},
        headers=headers
    )   
    print(res.json())

    return id_token
