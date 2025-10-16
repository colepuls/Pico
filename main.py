from local_llm.model import model as model
from skills.weather import get_weather
from skills.vision import take_picture
from skills.reminders import set_reminder
from skills.text_to_speech import speak
from skills.speech_to_text import record_audio
from skills.speech_to_text import translate_audio_to_text
from skills.get_current_time import get_time
import time
import sys

# Gives hard coded prints a typing effect in the cli
def typewriter(text, delay):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print("\n")

# ----- Main Program -----
def main():
    # Phrase loads
    weather_phrase = "weather"
    picture_phrase = "photo"
    set_remider_phrase = "reminder"
    current_time_phrase = "what time is it"

    # Asleep loop
    while True:
        awake = False
        wake_phrases = ["hey pico", "pico", "wake up"]
        # wake up pico
        print("---- Wake up Pico ----\n")
        while True:
            record_audio()
            input = translate_audio_to_text()
            if any(phrase in input.lower() for phrase in wake_phrases):
                awake = True
                break

        # Awake loop
        while awake:
            # get user_input
            print("---- Talk to Pico ----\n")
            record_audio()
            user_input = translate_audio_to_text()
            print("User: ", end="")
            typewriter(user_input, 0.03)

            # get skill outputs
            if weather_phrase in user_input.lower():
                temperature = get_weather(38.95, -92.33) # Columbia, MO
                typewriter(f"The temperature is {temperature} degrees farenheit.", 0.03)
                speak(f"The temperature is {temperature} degrees farenheit.")
                continue
            if current_time_phrase in user_input.lower():
                current_time = get_time()
                typewriter(f"The time is {current_time}", 0.03)
                speak(f"The time is {current_time}")
                continue
            if picture_phrase in user_input.lower():
                typewriter("Taking photo...", 0.03)
                take_picture("./images/photo.jpg")
                typewriter("Photo taken.", 0.03)
                continue

            # get model output
            print("Pico: ", end="")
            response = model(user_input)
            speak(response)