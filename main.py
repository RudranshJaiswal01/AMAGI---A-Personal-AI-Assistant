from ui.floating_widget import start_widget
from background.screen_watcher import start_screen_upload_loop
from background.voice_listener import start_voice_trigger # future update
from auth.google_login import google_login
from session.session_manager import save_session, load_session
import threading

# Login
session = load_session()
if not session:
    session = google_login()
    save_session(session)

# Background jobs
threading.Thread(target=start_screen_upload_loop, args=(session,), daemon=True).start()
threading.Thread(target=start_voice_trigger, args=(session,), daemon=True).start()

# UI
start_widget(session)
