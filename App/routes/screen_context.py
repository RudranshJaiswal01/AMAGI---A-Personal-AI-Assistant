#APP/routes/screen_context.py
import base64
from fastapi import APIRouter, Request, File, UploadFile, Form
from datetime import datetime

from App.utils.decorators import require_google_auth
from App.services.memory_store import save_memory
from App.services.groq_modules.img_descriptor import get_img_description

router = APIRouter()

@router.post("/screen/image")
@require_google_auth
async def upload_screen_context_image(
    request: Request,
    device_name: str = Form(...),
    device_id: str = Form(...),
    timestamp: str = Form(...),  # ISO format string from client
    image: UploadFile = File(...)
):
    try:
        user_id = request.state.user_id

        # Step 1: Read image and convert to base64
        img_bytes = await image.read()
        base64_img = base64.b64encode(img_bytes).decode("utf-8")
        image_data_url = f"data:image/png;base64,{base64_img}"

        # Step 2: Describe image using LLM
        description = get_img_description(image_data_url)  # Ignore `self`

        # Step 3: Save to memory
        save_memory(
            user_id=user_id,
            role="screen",
            text=f"Screen context from {device_name}:\n{description}",
            datetime=timestamp,
            source="screen_context",
            device_id=device_id
        )

        return {"status": "success"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
