import local_llm.model as model
import data_stream.audio_out as audio_out
import data_stream.speech_to_text as voice_in
from data_stream.text_to_speech import convert_text_to_audio
import wakeword.prep_model as wakeword_model
import skills.bibleverse as verse
import skills.date_time as date_time
import skills.joke as joke
import skills.movement as movement
import skills.system_report as report
import skills.weather as weather
from enum import Enum
from colorama import Fore, init; init()
import time


# Paths
PICO_VOICE_PATH = "/home/cole/Pico/audio_files/sound.wav"
CHIME_PATH = "/home/cole/Pico/audio_files/pico-chime2.wav"
LAUGH_PATH = "/home/cole/Pico/audio_files/laugh.wav"
PHOTO_PATH = "/home/cole/Pico/images/photo.jpg"


# Skill router
SKILLS = {
    "verse": verse.run_verse,
    "date": date_time.run_date,
    "time": date_time.run_time,
    "joke": joke.run_joke,
    "dance": movement.run_dance,
    "report": report.run_system_report,
    "weather": weather.run_weather
}

class State(Enum):
    SLEEPING = 0
    AWAKE = 1

class Robot:
    def __init__(self, state: State):
        self.name = "Pico"
        self.state = state
        
    def wake(self):
        self.state = State.AWAKE

    def sleep(self):
        self.state = State.SLEEPING
       
    @property    
    def awake(self):
        return self.state == State.AWAKE
        
    @property    
    def sleeping(self):
        return self.state == State.SLEEPING
     
        
def handle_input(user_input):
    words = set(user_input.lower().split()) # o(1)
    for phrase, skill in SKILLS.items():
        if phrase in words:
            
            text = skill()
            
            if phrase == "joke": # plays sound after response said, returns string, sound path
                return text, LAUGH_PATH
            
            return text, None
            
    return model.run(user_input), None


def printf(text, color):
    for c in text:
        print(color + c, end='', flush=True)
        time.sleep(0.01)
    print("\n\n")


def run_system():
    pico = Robot(State.SLEEPING)
    
    # System loop
    while True:
        
        # Asleep
        print(Fore.RED + "ASLEEP")
        print("\n")
        while pico.sleeping:
            data, sr, _ = voice_in.record_audio(sleep_delay=0.1) # check for audio every 100ms
            prob = wakeword_model.get_prob(data, sr)
            if prob > 0.50:
                pico.wake()
                break
            
        # Awake
        while pico.awake:
            print(Fore.GREEN + "AWAKE")
            print("\n")
            audio_out.play_audio(CHIME_PATH)
            _, _, speech_detected = voice_in.record_audio(sleep_delay=2.0) # wait for 2s then go back to sleep
            if not speech_detected:
                pico.sleep()
                break
            
            # Process input    
            user_input = voice_in.translate_audio_to_text().lower()
            printf(user_input, Fore.YELLOW)
            pico_output, after_sound = handle_input(user_input)
            convert_text_to_audio(pico_output)
            audio_out.play_audio(PICO_VOICE_PATH)
            if after_sound:
                audio_out.play_audio(after_sound)
            printf(pico_output, Fore.BLUE)
            pico.sleep()

            
if __name__ == '__main__':
    run_system()