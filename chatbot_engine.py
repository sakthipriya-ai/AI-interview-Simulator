from dotenv import load_dotenv
import os
from openai import OpenAI

# Load API key
load_dotenv(dotenv_path=".env")

api_key = os.getenv("OPENAI_API_KEY")

print("DEBUG API KEY:", api_key)

if not api_key:
    raise ValueError("❌ API KEY NOT LOADED")

client = OpenAI(api_key=api_key)

# Store chat memory
user_memory = {}

def get_chatbot_reply(user, message):

    if user not in user_memory:
        user_memory[user] = []

    # 🔥 SIMPLE FALLBACK LOGIC
    msg = message.lower()

    if "python" in msg:
        return "Python is a powerful language used in AI, web, and data science."

    elif "sql" in msg:
        return "SQL is used to manage and query databases."

    elif "machine learning" in msg:
        return "Machine Learning allows systems to learn from data."

    elif "interview" in msg:
        return "In interviews, explain concepts clearly with examples."

    elif "resume" in msg:
        return "A strong resume should highlight skills, projects, and achievements."

    else:
        return "Interesting question! Try answering with examples and real-world use cases."