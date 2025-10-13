from local_llm.model import model as model
from skills.weather import get_weather as get_weather
from skills.vision import take_picture as take_picture
from skills.motion import servo
from skills.motion import run_motor as run_motor
from skills.motion import stop_motor as stop_motor
import time
import sys

# function for giving skill pulls a type effect in the cli
def typewriter(text, delay):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print("\n")


def main():
    awake = True

    # phrase loads
    weather_phrase = "weather"
    picture_phrase = "photo"
    motor_start_phrase = "start motor"
    motor_stop_phrase = "stop motor"

    while awake:
        user_input = input("-> ") # get user input
        print()

        # skill pulls
        if weather_phrase in user_input.lower():
            temperature = get_weather(38.95, -92.33) # get columbia mo current temp
            typewriter(f"The temperature is {temperature} degrees farenheit.", 0.03)
            continue
        if picture_phrase in user_input.lower():
            typewriter("Taking photo...", 0.03)
            take_picture("./images/photo.jpg")
            typewriter("Photo taken.", 0.03)
            continue
        if motor_start_phrase in user_input.lower():
            typewriter("Running motor...", 0.03)
            run_motor()
            continue
        if motor_stop_phrase in user_input.lower():
            stop_motor()
            typewriter("Motor stopped.", 0.03)
            continue

        response = model(user_input) # get response to user input from ollama model
        
        print(response + "\n")