# app/routes/chat_text.py

from fastapi import APIRouter, Request
from pydantic import BaseModel
from datetime import datetime

from App.utils.decorators import require_google_auth
from App.services.memory_store import save_memory, search_memory
# from App.amagi_intelli import run_amagi

router = APIRouter()

class TextChatInput(BaseModel):
    prompt: str
    device_id: str
    device_name: str
    datetime: str  # from client (ISO format)

@router.post("/chat/text")
@require_google_auth
async def handle_text_chat(request: Request, data: TextChatInput):
    user_id = request.state.user_id
    prompt = data.prompt
    device_id = data.device_id
    device_name = data.device_name
    dt = data.datetime

    # Step 1: Retrieve relevant memory
    context_block = search_memory(user_id, prompt)

    # Step 2: Run reasoning model
    user_metadata = f"User metadeta: [device_name={device_name}, device_id={device_id}, datetime={dt}]"
    final_prompt = f"""
User Metadata:
- Device Name: {device_name}
- Device ID: {device_id}
- Datetime: {dt}

Relevant Memory:
{context_block}

User Prompt:
{prompt}
""".strip()

    # response = run_amagi(final_prompt)
    response = "this is the response"
    # Step 3: Save both query and reply
    save_memory(
        user_id=user_id,
        role="user",
        text=f"{user_metadata}\nUser: {prompt}",
        datetime=dt,
        source="text_chat",
        device_id=device_id
    )

    save_memory(
        user_id=user_id,
        role="amagi",
        text=response,
        datetime=dt,
        source="text_chat",
        device_id=device_id
    )

    return {"response": response}
