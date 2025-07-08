import os
from App.services.groq_modules.groq_client import client

def to_speech(text, user_id):
    # Overwrite file each time per user
    filename = f"{user_id}_amagi_response.mp3"
    speech_file_path = os.path.join("static", "speech_outputs", filename)

    response = client.audio.speech.create(
        model="playai-tts",
        voice="Jennifer-PlayAI",
        response_format="mp3",
        input=text
    )

    response.write_to_file(speech_file_path)

    return filename
