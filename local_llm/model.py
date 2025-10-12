import ollama

def model(user_input):

    response = ollama.chat(
        model='qwen2.5:0.5b',
        messages=[
            {
                'role': 'user',
                'content': user_input
            }
        ],
        stream=True
    )

    return response
