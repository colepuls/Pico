from local_llm.model import model as model
from skills.weather import get_weather
#from skills.photo import take_picture
from skills.text_to_speech import speak
from skills.speech_to_text import record_audio
from skills.speech_to_text import translate_audio_to_text
from skills.get_current_time import get_time
from skills.wakeword.wakeword_runtime import get_prob
from skills.play_sounds import play_sound
from skills.joke import tell_a_joke
from skills.system_report import get_system_report
from skills.bibleverse import get_random_verse
from skills.motion import dance
from skills.reportdevlog import read_last_devlog
from screen import switch_state
from screen import set_dash_screen
from colorama import Fore
import time as t

def animate_print(text, delay, color):
    for c in text:
        print(color + c, end='', flush=True)
        t.sleep(delay)
    print("\n")

def get_response(user_input):

    weather_phrase = "weather"
    picture_phrase = "photo"
    current_time_phrase = "time"
    joke_phrase = "joke"
    system_report_phrase = "report"
    bible_verse_phrase = "verse"
    dance_phrase = "dance"
    track_phrase = "track"
    devlog_phrase = "log"
    switch_state_phrase = "switch state"

    if switch_state_phrase in user_input.lower():
        response = "Switching state"
        speak(response)
        switch_state()
        return response, False

    if weather_phrase in user_input.lower():
        response = get_weather(38.95, -92.33) # Columbia, MO
        speak(response)
        return response, False
    
    if devlog_phrase in user_input.lower():
        response = read_last_devlog()
        speak(response)
        return response, False

    if joke_phrase in user_input.lower():
        response = tell_a_joke()
        speak(response)
        play_sound("/home/colecodes/projects/Pico/audio_files/laugh.wav")
        return response, False
    
    # Putting this off for now, going to move servo control to arduino instead
    if track_phrase in user_input.lower():
        response = "Tracking"
        speak(response)
        # track function, thread
        return response, False

    if current_time_phrase in user_input.lower():
        response = get_time()
        speak(response)
        return response, False
    
    if system_report_phrase in user_input.lower():
        response = get_system_report()
        speak(response)
        return response, False
    
    if bible_verse_phrase in user_input.lower():
        response = get_random_verse()
        speak(response)
        return response, False
    
    if dance_phrase in user_input.lower():
        response = "Boom shakalaka"
        speak(response)
        dance()
        return response, False


    # NOTE: Needs to be threaded or stop live video feed when called
    if picture_phrase in user_input.lower():
        response = "Taking photo"
        speak(response)
        #take_picture('/home/colecodes/projects/Pico/images/photo.jpg')
        return response, False

    # Get llm response
    response = model(user_input)
    speak(response)
    return response, True

def main():
    """
    This is the main loop conversation loop with Pico.
        - Constantly waits for wakeword.
        - Once wakeword is detected Pico 'wakes up' and runs awake loop.
        - Awake loop will take user input (voice) and use one of the skill responses or llm response.
    """

    set_dash_screen()

    awake = False

    while True:

        # Asleep loop
        #print(Fore.RED + "Asleep (wake up pico)")
        #print(Fore.RED + "---------------------\n")
        while awake == False:
            data, sr, _ = record_audio(stime=0.1)
            prob_wakeword = get_prob(data, sr)
            if prob_wakeword > 0.80: # if wakeword was predicted wake up robot
                awake = True
                break

        # Awake loop
        #print(Fore.GREEN + "Awake (listening)")
        #print(Fore.GREEN + "-----------------\n")
        while awake == True:
            play_sound("/home/colecodes/projects/Pico/audio_files/pico-chime2.wav") # play wake chime
            _, _, speech_detected = record_audio(stime=2.0) # get user input
            if not speech_detected: # if no speech detected go back to sleep
                awake = False
                break

            #print(Fore.YELLOW + "User")
            #print(Fore.YELLOW + "----")
            user_input = translate_audio_to_text().lower()
            #animate_print(f"{user_input}", 0.02, Fore.YELLOW)

            #print(Fore.BLUE + "Pico")
            #print(Fore.BLUE + "----")
            response, is_llm = get_response(user_input)
            if is_llm == True:
                awake = False
                break
            if is_llm == False:
                #animate_print(f"{response}", 0.02, Fore.BLUE)
                awake = False
                break

if __name__ == '__main__':
    main()

# TODO:
"""
- Dance
- Wake animation (already have chime maybe add some visual and motor movement)
- Gesture recognition (wake when waved at)
- Face detection, have pico recognize different people
- Add to where when user does not say anything for 3 minitues pico's visual display goes to sleep
- Add proper motion control
- 3d print parts
- Create visual screen
- Assemble all the parts
- IDLE behaviors
- Github notifier "You have 2 new commits pushed to 'repo'."
- Auto-greeting (when face detected)
- Follow movement (turn to look at person if moving around room)
- Fix camera colors
- Add model visual (create website showcasing Pico)
"""