# actllama -> shortcut cmd for venv
from llama_cpp import Llama
import os, sys

PATH = "/home/colecodes/projects/Pico/llm/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf" # model path
MODEL = PATH

# configuration
llm = Llama(
    model_path=MODEL,
    n_ctx=1024, # cash context I think
    n_threads=os.cpu_count(), # use all of pi's cores
    n_batch=128, # tuning
    use_mlock =False,
    embedding=False,
    verbose=False # prevent info overload
)

print("Ask Pico")

while True:
    try:
        user = input("-> ") # type prompt
    except KeyboardInterrupt: # ctrl c to exit
        sys.exit(0)

    messages = [{"role": "system", "content":"You are a concise, helpful assistant."}, {"role": "user", "content": user}]
    for token in llm.create_chat_completion(
        messages=messages,
        max_tokens = 220,
        temperature = 0.6,
        top_p = 0.9,
        stream=True
    ):
        print(token["choices"][0]["delta"].get("content",""), end="", flush=True) # print letter by letter
    print("\n")