# actllama -> shortcut cmd for venv
from llama_cpp import Llama
import os, sys

PATH = "/home/colecodes/projects/Pico/llm/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf" # model path
MODEL = PATH

# configuration
llm = Llama(
    model_path=MODEL,
    n_ctx=2048, # cash context
    n_threads=os.cpu_count(), # use all of pi's cores
    n_batch=128, # tuning
    use_mlock =False,
    embedding=False,
    verbose=False,
    chat_format="chatml", # for tinyllama chat
)

print("Ask Pico")

# inference parameters
GEN_KW = dict(
    max_tokens=300,
    temperature=0.2, # low temp reduces hallucinations
    top_p=0.85,
    top_k=40,
    repeat_penalty=1.12,
    seed=42,
    stop=["<|im_end|>", "</s>"]
)

greetings = {"hi", "hello", "hey", "yo", "sup"}
who = {"who are you", "what's your name", "what is your name"}

while True:
    try:
        user = input("-> ")
    except KeyboardInterrupt: # ctrl c to exit
        print()
        sys.exit(0)

    if user in greetings:
        print("Hello, i'm Pico.\n")
        continue
    elif user in who:
        print("My name is Pico, your friendly AI assistant.\n")
        continue

    messages = [
        {"role": "system", "content": user}
    ]

    try:
        for token in llm.create_chat_completion(
            messages=messages,
            stream=True,
            **GEN_KW
        ):
            print(token["choices"][0]["delta"].get("content", ""), end="", flush=True)
        print("\n")
    except KeyboardInterrupt:
        print("\n")  # break long response
    except Exception as e:
        print(f"\n[Error] {e}\n")