from local_llm.model import model as model
from skills.weather import get_weather
from skills.photo import take_picture
from skills.text_to_speech import speak
from skills.speech_to_text import record_audio
from skills.speech_to_text import translate_audio_to_text
from skills.get_current_time import get_time
from skills.photo import take_picture
from skills.wakeword.wakeword_runtime import get_prob
from skills.play_sounds import play_sound
from skills.joke import tell_a_joke
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
    joke_phrase = "joke"

    # ---------- Robot loop ----------
    while True:
        # ---------- Asleep loop ----------
        awake = False
        print("---- Wake up Pico ----\n")
        while awake == False:
            data, sr, _ = record_audio(stime=0.1)
            prob_wakeword = get_prob(data, sr)
            if prob_wakeword > 0.80: # if wakeword was predicted wake up robot
                awake = True
                break

        # ---------- Awake loop ----------
        while awake == True:
            play_sound("/home/colecodes/projects/Pico/audio_files/pico-chime2.wav") # play wake chime
            print("---- Talk to Pico ----\n")
            _, _, speech_detected = record_audio(stime=2.0) # get user input

            if not speech_detected: # if no speech detected go back to sleep
                awake = False
                break

            user_input = translate_audio_to_text()
            print("User: ", end="")
            typewriter(user_input, 0.03)

            # Get a skill response
            if weather_phrase in user_input.lower():
                weather = get_weather(38.95, -92.33) # Columbia, MO
                typewriter(f"{weather}", 0.03)
                speak(f"{weather}")
                awake = False
                break

            if joke_phrase in user_input.lower():
                joke = tell_a_joke()
                typewriter(f"{joke}", 0.03)
                speak(f"{joke}")
                play_sound("/home/colecodes/projects/Pico/audio_files/laugh.wav")
                awake = False
                break

            if current_time_phrase in user_input.lower():
                current_time = get_time()
                typewriter(f"The time is {current_time}", 0.03)
                speak(f"The time is {current_time}")
                awake = False
                break

            # Needs to be threaded or stop live video feed when called
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