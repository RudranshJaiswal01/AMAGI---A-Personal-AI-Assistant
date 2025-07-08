import os
from groq import Groq
from App.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)