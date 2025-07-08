#APP/services/stt_model.py
from App.services.groq_modules.groq_client import client

def get_transcript(self, filepath, prompt=""):
    try:
        with open(filepath, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(filepath, file.read()),
                model="whisper-large-v3",
                prompt=prompt,
                language="en"
            )
        print(transcription.text)
        return transcription.text

    except Exception as e:
        print("Error: ", e)
        return "Sorry, some error occured! Please try again."