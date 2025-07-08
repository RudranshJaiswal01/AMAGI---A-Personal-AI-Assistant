import os
import uuid
import shutil
from fastapi import APIRouter, Request, UploadFile, File, Form

from App.utils.decorators import require_google_auth
from App.services.memory_store import save_memory, search_memory
from App.services.groq_modules.stt_model import get_transcript
from App.services.groq_modules.tts_model import to_speech
# from App.amagi_intelli import run_amagi

router = APIRouter()

@router.post("/chat/voice")
@require_google_auth
async def handle_voice_chat(
    request: Request,
    audio: UploadFile = File(...),
    device_id: str = Form(...),
    device_name: str = Form(...),
    timestamp: str = Form(...),
):
    user_id = request.state.user_id

    # Step 1: Save uploaded audio to temp file
    temp_filename = f"temp_{uuid.uuid4()}.wav"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    # Step 2: Transcribe audio
    transcript = get_transcript(temp_filename)
    if transcript.strip() == "":
        return {"error": "Empty or failed transcription"}

    # Step 3: Retrieve relevant memory
    memory_context = search_memory(user_id, transcript)

    # Step 4: Run reasoning model
    user_metadata = f"""
User Metadata:
- Device Name: {device_name}
- Device ID: {device_id}
- Datetime: {timestamp}
""".strip()

    final_prompt = f"{user_metadata}\nRelevant Memory:\n{memory_context}\n\nUser Said:\n{transcript}"
    response = "This is the response." # run_amagi(final_prompt)

    # Step 5: Convert response to speech
    speech_filename = to_speech(response, user_id)
    public_url = f"/speech_outputs/{speech_filename}"

    # Step 6: Save to memory
    save_memory(
        user_id=user_id,
        role="user",
        text=f"{user_metadata}\nUser: {transcript}",
        datetime=timestamp,
        source="voice_chat",
        device_id=device_id,
    )
    save_memory(
        user_id=user_id,
        role="amagi",
        text=response,
        datetime=timestamp,
        source="voice_chat",
        device_id=device_id,
    )

    # Step 7: Cleanup temp
    os.remove(temp_filename)

    return {
        "response": response,
        "audio_url": public_url,
    }
