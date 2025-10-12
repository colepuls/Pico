from local_llm.model import model as model

def main():
    user_input = input("-> ") # get user input
    print()
    response = model(user_input) # get response to user input from ollama model
    
    # print response word by word
    for word in response:
        print(word['message']['content'], end='', flush=True)

    print()