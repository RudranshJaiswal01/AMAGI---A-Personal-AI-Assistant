import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
HF_ACCESS_TOKEN = os.getenv("HF_ACCESS_TOKEN")

host = "127.0.0.1"
# host = "0.0.0.0"
port = 8000