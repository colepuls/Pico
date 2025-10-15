from openai import OpenAI
import os
from dotenv import load_dotenv
import sounddevice as sd
import soundfile as sf
import numpy as np

def record_audio():
    samplerate = 16000 # audio-samples/second, represents soundwaves
    threshold = 0.3 # how quiet the sound needs to be to count as 'silence'
    silence_time = 2 # how long in seconds silence must lasts before stopping
    block_size = 1024 # grab 1024 audio-samples at a time
    silence_time_tracker = 0 # silence time tracker
    audio = [] # stores all recorded chunks

    print("Start talking...")

    # open microphone stream
    with sd.InputStream(samplerate=samplerate, channels=1) as stream:
        while True:
            block = stream.read(block_size)[0] # reads one chunk of audio from the mic
            volume = np.linalg.norm(block) # computes magnitude of the vector giving us a volume for that block
            audio.append(block)
            if volume < threshold:
                silence_time_tracker += block_size / samplerate
                if silence_time_tracker > silence_time:
                    break
            else:
                silence = 0
        
    data = np.concatenate(audio, axis=0) # combine all audio chunks
    sf.write("audio.wav", data, samplerate)


def translate_audio_to_text():
    load_dotenv()

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=OPENAI_API_KEY)

    with open("audio.wav", "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=f,
            response_format="text"
        )

    return transcript

def main():
    record_audio()
    text = translate_audio_to_text()
    speak(text)

if __name__ == '__main__':
    main()