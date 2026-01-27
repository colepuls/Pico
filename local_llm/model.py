import ollama
import json
import os

MEMORY_FILE = "/home/cole/Pico/local_llm/memory.json"

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
        json.dump(memory[-4:], f) # keep last 4 messages, not counting the system prompt

def run(user_input):
    PERSONALITY = "You are Pico, a kind, goofy chatbot that gives clear and concise answers, and say stupid jokes whenever feasable. Keep a conversational tone and remember the past chats naturally. You speak ENGLISH only."
    MODEL = "qwen2.5:0.5b"

    memory = load_memory()

    system_message = {'role': 'system', 'content': PERSONALITY}
    user_message = {'role': 'user', 'content': user_input}

    messages = [
        system_message,
        *memory, # unpackages the dictionary.
        user_message
    ]

    res = ollama.chat(model=MODEL, messages=messages)
    response = res["message"]["content"]
    
    response_message = {'role': 'assistant', 'content': response}

    memory.append(user_message)
    memory.append(response_message)
    save_memory(memory)

    return response
