import tkinter as tk
from tkinter import simpledialog
import threading
import requests

from config import host, port

class AmagiApp:
    def __init__(self, session):
        self.session = session
        self.root = tk.Tk()
        self.root.title("Amagi")
        self.root.overrideredirect(True)  # Remove title bar
        self.root.attributes("-topmost", True)
        self.root.geometry("120x60+100+100")

        self.chat_open = False

        self.frame = tk.Frame(self.root, bg="black")
        self.frame.pack(fill="both", expand=True)

        self.chat_btn = tk.Button(self.frame, text="Chat", command=self.toggle_chat)
        self.chat_btn.pack(side="left", padx=5, pady=5)

        self.voice_btn = tk.Button(self.frame, text="Voice", command=self.voice_input)
        self.voice_btn.pack(side="right", padx=5, pady=5)

        self.frame.bind("<ButtonPress-1>", self.start_move)
        self.frame.bind("<B1-Motion>", self.do_move)

        self.root.mainloop()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def toggle_chat(self):
        if self.chat_open:
            self.chat_win.destroy()
            self.chat_open = False
        else:
            self.chat_open = True
            self.chat_win = tk.Toplevel(self.root)
            self.chat_win.title("Chat with Amagi")
            self.chat_win.geometry("300x400")
            self.chat_win.attributes("-topmost", True)

            self.chat_text = tk.Text(self.chat_win, height=20)
            self.chat_text.pack()

            self.entry = tk.Entry(self.chat_win)
            self.entry.pack(fill="x")

            send_btn = tk.Button(self.chat_win, text="Send", command=self.send_message)
            send_btn.pack()

    def send_message(self):
        msg = self.entry.get()
        self.chat_text.insert(tk.END, f"You: {msg}\n")
        self.entry.delete(0, tk.END)

        res = requests.post(
            f"http://{host}:{port}/chat/text",
            headers={"Authorization": f"Bearer {self.session['id_token']}"},
            json={
                "prompt": msg,
                "device_id": "laptop-123",
                "device_name": "MyLaptop",
                "datetime": "2025-07-06T12:00:00"
            }
        )
        if res.ok:
            reply = res.json()['response']
            self.chat_text.insert(tk.END, f"Amagi: {reply}\n")

    def voice_input(self):
        print("Voice button clicked")
        # Trigger audio capture and send to server

def start_widget(session):
    AmagiApp(session)
