# Imports
from openai import OpenAI
from dotenv import load_dotenv
from pydub.playback import play
from pydub import AudioSegment
import sounddevice as sd
import soundfile as sf
import numpy as np
import tempfile
import os
import io

# Create api client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Indication sound
def beep(frequency=1000, duration=0.2, sr=44100):
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    wave = 0.2 * np.sin(2 * np.pi * frequency * t)  # 0.2 = volume
    sd.play(wave, sr)
    sd.wait()

wake_phrases = ["pico", "hey pico", "wake", "wake up"]
awake = False

# Wait for wake word
def wait_for_wake():
    global awake
    print("Wake Pico to start\n")
    sr = 16000
    while True:
        # short listen window
        audio = sd.rec(int(2*sr), samplerate=sr, channels=1, dtype="int16")
        sd.wait()

        p = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
        sf.write(p, audio, sr, subtype="PCM_16")

        try:
            txt = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=open(p, "rb"),
                response_format="text",
                language="en"
            ).strip().lower()
        finally:
            os.remove(p)

        if any(phrase in txt for phrase in wake_phrases):
            awake = True
            beep()
            return

# Record user voice input and convert to text
def speech_to_text():
    print("Ask Pico\n")
    sr = 16000 # sample rate
    max_secs = 15
    silence_len = 1.0 # stop listening after 5 seconds of silence

    block = int(sr * 0.25)  # check every 0.25s
    frames = []
    silent_time = 0.0

    with sd.InputStream(samplerate=sr, channels=1, dtype="int16") as stream:
        for _ in range(int(max_secs / 0.25)):
            data, _ = stream.read(block)
            frames.append(data.copy())

            rms = np.sqrt(np.mean(data.astype(np.float32)**2))
            if rms < 50:    
                silent_time += 0.25
            else:
                silent_time = 0.0

            if silent_time >= silence_len:
                break

    audio = np.concatenate(frames, axis=0)

    # ignore near silence
    rms = np.sqrt(np.mean(audio.astype(np.float32)**2))
    if rms < 50:    
        return ""

    p = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    sf.write(p, audio, sr, subtype="PCM_16")
    txt = OpenAI().audio.transcriptions.create(model="gpt-4o-mini-transcribe", language="en", file=open(p,"rb"), response_format="text")
    print("User: ", txt)
    print("\n")

    return txt


# Give model user input and get back model's response
def get_response(text):
    print("Thinking...\n")
    response = client.responses.create(
        model="gpt-3.5-turbo",
        input = text
    )

    output = response.output_text

    return output

# Convert model's response to audio
def text_to_speech(model_output):
    print("Pico: ", model_output)
    print("\n")
    response = client.audio.speech.create(
        model = "gpt-4o-mini-tts",
        voice = "ash",
        input = model_output
    )

    audio_bytes = response.read()
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")

    return audio

def play_blocking(audio_segment):
    samples = np.array(audio_segment.get_array_of_samples())
    if audio_segment.channels == 2:
        samples = samples.reshape((-1, 2))
    sd.play(samples, audio_segment.frame_rate)
    sd.wait() 

# Play audio, goes to main.py
def run(text, model_output, pico_audio):
    play_blocking(pico_audio)
