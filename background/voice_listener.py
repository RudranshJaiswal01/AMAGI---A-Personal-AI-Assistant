import speech_recognition as sr
import requests
import tempfile
import os
from datetime import datetime

from config import host, port

def start_voice_trigger(session):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        try:
            with mic as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)

                print("Heard:", text)

                if "amagi" in text.lower():
                    print("Trigger detected!")
                    now = datetime.now().isoformat()

                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                        f.write(audio.get_wav_data())
                        f.flush()

                        with open(f.name, "rb") as voice:
                            files = {"audio": ("voice.wav", voice, "audio/wav")}
                            data = {
                                "device_id": "laptop-123",
                                "timestamp": now
                            }
                            headers = {"Authorization": f"Bearer {session['id_token']}"}
                            requests.post(f"http://{host}:{port}/chat/voice", data=data, files=files, headers=headers)

                        os.unlink(f.name)

        except Exception as e:
            print("Voice trigger error:", e)
