# run_server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from App.routes import auth, chat_text, chat_voice, screen_context
from App.config import host, port

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(auth.router)
app.include_router(chat_text.router)
app.include_router(chat_voice.router)
app.include_router(screen_context.router)

# Serve TTS outputs
app.mount("/speech_outputs", StaticFiles(directory="static/speech_outputs"), name="speech_outputs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("run_server:app", host=host, port=port, reload=True)
