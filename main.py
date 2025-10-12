from local_llm.model import model as model
from skills.weather import get_weather as get_weather

def main():
    # phrase loads
    weather_phrase = "weather"

    user_input = input("-> ") # get user input
    print()

    if weather_phrase in user_input.lower():
        temperature = get_weather(38.95, -92.33) # get columbia mo current temp
        print(f"The temperature is {temperature} degrees farenheit.\n")
        return

    response = model(user_input) # get response to user input from ollama model
    
    # print response word by word
    for word in response:
        word = word['message']['content']
        print(word, end='', flush=True)

    print()