from local_llm.model import model as model
from skills.weather import get_weather as get_weather
from skills.vision import take_picture as take_picture
from skills.motion import servo
from skills.motion import run_motor as run_motor
from skills.motion import stop_motor as stop_motor
from skills.reminders import set_reminder as set_reminder
from skills.text_to_speech import speak as speak
from skills.speech_to_text import record_audio as record_audio
from skills.speech_to_text import translate_audio_to_text as translate_audio_to_text
from skills.get_time import get_current_time as get_current_time
import time
import sys

# function for giving skill pulls a type effect in the cli
def typewriter(text, delay):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print("\n")

def main():
    while True:
        awake = False
        wake_phrase = "hey pico"
        # wake up pico
        print("---- Wake up Pico ----\n")
        while True:
            record_audio()
            input = translate_audio_to_text()
            if wake_phrase in input.lower():
                awake = True
                break

        while awake:
            # phrase loads
            weather_phrase = "weather"
            picture_phrase = "photo"
            motor_start_phrase = "start motor"
            motor_stop_phrase = "stop motor"
            set_remider_phrase = "reminder"
            current_time_phrase = "what time is it"

            # get user_input
            print("---- Talk to Pico ----\n")
            record_audio()
            user_input = translate_audio_to_text()
            print("User: ", end="")
            typewriter(user_input, 0.03)

            # get skill outputs
            if weather_phrase in user_input.lower():
                temperature = get_weather(38.95, -92.33) # get columbia mo current temp
                typewriter(f"The temperature is {temperature} degrees farenheit.", 0.03)
                speak(f"The temperature is {temperature} degrees farenheit.")
                awake = False
                continue
            if current_time_phrase in user_input.lower():
                current_time = get_current_time()
                typewriter(f"The time is {current_time}.", 0.03)
                speak(f"The time is {current_time}.")
                awake = False
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
            if set_remider_phrase in user_input.lower():
                typewriter("Set reminder", 0.03)
                year = int(input("Year: "))
                month = int(input("Month: "))
                day = int(input("Day: "))
                hour = int(input("Hour: "))
                minute = int(input("Minute: "))
                reminder_message = input("Message: ")
                set_reminder(year, month, day, hour, minute, reminder_message)
                continue
            if user_input.strip() == "":
                typewriter(f"[Reminder] {reminder_message}", 0.03)
                speak(reminder_message)
                continue

            # get model output
            print("Pico: ", end="")
            response = model(user_input)
            speak(response)
            awake = False