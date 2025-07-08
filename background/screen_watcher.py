import time
import pyautogui
import base64
import requests
from io import BytesIO
from datetime import datetime

from config import host, port

def start_screen_upload_loop(session):
    while True:
        try:
            screenshot = pyautogui.screenshot()
            buffer = BytesIO()
            screenshot.save(buffer, format="PNG")
            buffer.seek(0)

            now = datetime.now().isoformat()

            files = {"image": ("screenshot.png", buffer, "image/png")}
            data = {
                "device_name": "MyLaptop",
                "device_id": "laptop-123",
                "timestamp": now
            }

            headers = {"Authorization": f"Bearer {session['id_token']}"}
            res = requests.post(f"http://{host}:{port}/screen/image", data=data, files=files, headers=headers)
            print("Screen upload response:", res.status_code)
            print("Status:", res.json().get("status"))
            
        except Exception as e:
            print("Screen upload failed:", e)

        time.sleep(1)
