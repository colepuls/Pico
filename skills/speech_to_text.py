from openai import OpenAI
import os
from dotenv import load_dotenv
import sounddevice as sd
import soundfile as sf
import numpy as np

def record_audio(stime):
    """
    This function records user input and stores into a .wav file.
    """

    samplerate = 16000
    threshold = 0.3
    silence_time = stime
    block_size = 1024
    silence_time_tracker = 0
    audio = []

    # Open mic stream
    with sd.InputStream(samplerate=samplerate, channels=1) as stream:
        while True:
            block = stream.read(block_size)[0]
            volume = np.linalg.norm(block) 
            audio.append(block)
            if volume < threshold:
                silence_time_tracker += block_size / samplerate
                if silence_time_tracker > silence_time:
                    break
            else:
                silence = 0
        
    data = np.concatenate(audio, axis=0) # combine all audio chunks
    sf.write("/home/colecodes/projects/Pico/audio_files/audio.wav", data, samplerate)
    return data, samplerate

def translate_audio_to_text():
    """
    This is a speech-to-text function using openai's gpt-4o-transcribe model.
    - This works much better than any local model due to rasppi's hardware limitations.
    - Function loads .wav file from record_audio() and translates audio to text.
    """

    load_dotenv()

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=OPENAI_API_KEY)

    with open("/home/colecodes/projects/Pico/audio_files/audio.wav", "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=f,
            response_format="text"
        )

    return transcript