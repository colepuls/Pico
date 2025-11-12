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
from colorama import Fore, init; init()

def log(text):
    with open("chatlog.txt", "a") as f:
        f.write(text)

def get_response(user_input):

    weather_phrase = "weather"
    picture_phrase = "photo"
    current_time_phrase = "time"
    joke_phrase = "joke"

    if weather_phrase in user_input.lower():
        response = get_weather(38.95, -92.33) # Columbia, MO
        # print(f"{Fore.BLUE}{response}\n")
        log(f"{response}\n\n")
        speak(response)
        return response

    if joke_phrase in user_input.lower():
        response = tell_a_joke()
        # print(f"{Fore.BLUE}{response}\n")
        log(f"{response}\n\n")
        speak(response)
        play_sound("/home/colecodes/projects/Pico/audio_files/laugh.wav")
        return response


    if current_time_phrase in user_input.lower():
        response = get_time()
        # print(f"{Fore.BLUE}{response}\n")
        log(f"{response}\n\n")
        speak(response)
        return response

    # NOTE: Needs to be threaded or stop live video feed when called
    if picture_phrase in user_input.lower():
        print(f"{Fore.BLUE}Taking photo...\n")
        take_picture("./images/photo.jpg")
        print(f"{Fore.BLUE}Photo taken.\n")

    # Get llm response
    response = model(user_input)
    # print(f"{Fore.BLUE}{response}\n")
    log(f"{response}\n\n")
    speak(response)
    return response

def main():
    """
    This is the main loop conversation loop with Pico.
        - Constantly waits for wakeword.
        - Once wakeword is detected Pico 'wakes up' and runs awake loop.
        - Awake loop will take user input (voice) and use one of the skill responses or llm response.
    """

    awake = False

    while True:

        # ---------- Asleep loop ----------
        # print(f"{Fore.RED}---- Wake up Pico ----\n")
        log("---------- Wake up Pico ----------\n")
        while awake == False:
            data, sr, _ = record_audio(stime=0.1)
            prob_wakeword = get_prob(data, sr)
            if prob_wakeword > 0.80: # if wakeword was predicted wake up robot
                awake = True
                break

        # ---------- Awake loop ----------
        while awake == True:
            play_sound("/home/colecodes/projects/Pico/audio_files/pico-chime2.wav") # play wake chime
            # print(f"{Fore.GREEN}---- Talk to Pico ----\n")
            log("----------- Talk to Pico -----------\n\n")
            _, _, speech_detected = record_audio(stime=2.0) # get user input

            if not speech_detected: # if no speech detected go back to sleep
                awake = False
                break

            user_input = translate_audio_to_text()
            # print(f"{Fore.YELLOW}{user_input}")
            log(f"{user_input}\n\n")

            get_response(user_input)

            awake = False
            break

if __name__ == '__main__':
    main()

"""
TO DO:
- System report (CPU temp/usage, uptime, connection speed, RAM)
- Play music
- Reminders & Alarms
- Today's news summarizer
- Easter eggs: Hidden phrases that trigger funny responses
- Dance
- Wake animation (already have chime maybe add some visual and motor movement)
- Gesture recognition
- Face detection, have pico recognize different people
- Add to where when user does not say anything for 3 minitues pico's visual display goes to sleep
- Add proper motion control
- 3d print parts
- Update web server to show more things
- Give pico a visual face (eyes)
- Assemble all the parts
- Daily Bible verse
- IDLE behaviors
- Github notifier "You have 2 new commits pushed to 'repo'."
- Ambient noise (rain, forest)
- Auto-greeting (when face detected)
- Follow movement (turn to look at person if moving around room)
- Move code files + venv to new profile (desktop corrupt on current profile, need desktop to setup display)
- Fix camera colors
- Add model visual to server
"""