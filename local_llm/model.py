import ollama
import json
import os
from dotenv import load_dotenv

load_dotenv()

MEMORY_FILE = os.getenv("MEMORY_FILE")

# load memory for model
def load_memory():
    global MEMORY_FILE
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE) as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    else:
        return []

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory[-10:], f) # keep last 10 chats


def model(user_input):
    PERSONALITY = "You are Pico, a kind, goofy chatbot that gives clear and concise answers. Keep a conversational tone and remember the past chats naturally."

    MODEL = "qwen2.5:0.5b"

    memory = [{'role': 'system', 'content': PERSONALITY}]
    memory += load_memory()
    memory.append({'role': 'user', 'content': user_input})

    response = ""
    for word in ollama.chat(model=MODEL, messages=memory, stream=True):
        content = word["message"]["content"]   
        print(content, end="", flush=True)
        response += content

    memory.append({'role': 'assistant', 'content': response})
    save_memory(memory)

    return response
