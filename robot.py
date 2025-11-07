from local_llm.model import model as model
from skills.weather import get_weather
from skills.photo import take_picture
from skills.text_to_speech import speak
from skills.speech_to_text import record_audio
from skills.speech_to_text import translate_audio_to_text
from skills.get_current_time import get_time
from skills.photo import take_picture
from skills.wakeword.wakeword_runtime import get_prob
import time

def typewriter(text, delay):
    """
    This function gives hard coded prints a typing effect in the CLI.
    """
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print("\n")

def main():
    """
    This is the main loop conversation loop with Pico.
        - Constantly waits for wakeword.
        - Once wakeword is detected Pico 'wakes up' and runs awake loop.
        - Awake loop will take user input (voice) and use one of the skill responses or llm response.
    """

    # Skill phrase loads
    weather_phrase = "weather"
    picture_phrase = "photo"
    current_time_phrase = "time"

    # ---------- Robot loop ----------
    while True:
        awake = False
        print("---- Wake up Pico ----\n")
        # ---------- Asleep loop ----------
        while awake == False:
            data, sr = record_audio(stime=0.1)
            prob_wakeword = get_prob(data, sr)
            if prob_wakeword > 0.80:
                awake = True
                break

        # ---------- Awake loop ----------
        while awake == True:
            # Get user_input
            print("---- Talk to Pico ----\n")
            record_audio(stime=2.0)
            user_input = translate_audio_to_text()
            print("User: ", end="")
            typewriter(user_input, 0.03)

            # Get a skill response
            if weather_phrase in user_input.lower():
                temperature = get_weather(38.95, -92.33) # Columbia, MO
                typewriter(f"The temperature is {temperature} degrees farenheit.", 0.03)
                speak(f"The temperature is {temperature} degrees farenheit.")
                awake = False
                break
            if current_time_phrase in user_input.lower():
                current_time = get_time()
                typewriter(f"The time is {current_time}", 0.03)
                speak(f"The time is {current_time}")
                awake = False
                break
            if picture_phrase in user_input.lower():
                typewriter("Taking photo...", 0.03)
                take_picture("./images/photo.jpg")
                typewriter("Photo taken.", 0.03)
                awake = False
                break

            # Get llm response
            print("Pico: ", end="")
            response = model(user_input)
            speak(response)
            awake = False
            break