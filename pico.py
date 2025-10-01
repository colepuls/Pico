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
def coin_beep(sr=44100):
    dur1, dur2 = 0.1, 0.1
    t1 = np.linspace(0, dur1, int(sr*dur1), endpoint=False)
    t2 = np.linspace(0, dur2, int(sr*dur2), endpoint=False)
    wave1 = 0.2 * np.sin(2*np.pi*800*t1)
    wave2 = 0.2 * np.sin(2*np.pi*1200*t2)
    wave = np.concatenate([wave1, wave2])
    sd.play(wave, sr)
    sd.wait()

wake_phrases = ["pico", "hey pico"]
awake = False

# Wait for wake word
def wait_for_wake():
    global awake
    print("Wake Pico to start\n")
    sr = 16000
    gain = 10.0          # <<< mic boost (try 3–10)
    quiet_rms = 0.005   # <<< skip API call if below this (tune 0.003–0.01)

    while True:
        # short listen window
        audio = sd.rec(int(2*sr), samplerate=sr, channels=1, dtype="int16")
        sd.wait()

        # Convert to float [-1,1], apply gain, soft-limit
        audio_f32 = (audio.astype(np.float32) / 32768.0) * gain
        peak = float(np.max(np.abs(audio_f32)) + 1e-12)
        if peak > 0.99:
            audio_f32 /= peak / 0.99  # simple limiter

        # Quick silence gate to avoid wasting API calls
        rms = float(np.sqrt(np.mean(audio_f32**2)))
        if rms < quiet_rms:
            continue

        p = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
        sf.write(p, audio_f32, sr, subtype="PCM_16")

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
            coin_beep()
            return

# Record user voice input and convert to text
def speech_to_text():
    print("Ask Pico\n")
    sr = 16000 # sample rate
    max_secs = 15
    silence_len = 1.0 # stop listening after 1 second of silence

    block = int(sr * 0.25)  # check every 0.25s
    frames = []
    silent_time = 0.0
    gain = 10.0  # boost mic (tune 3–10)

    with sd.InputStream(samplerate=sr, channels=1, dtype="int16") as stream:
        for _ in range(int(max_secs / 0.25)):
            data, _ = stream.read(block)
            frames.append(data.copy())

            # Boost before measuring
            rms = np.sqrt(np.mean((data.astype(np.float32) * gain) ** 2))
            if rms < 20:
                silent_time += 0.25
            else:
                silent_time = 0.0

            if silent_time >= silence_len:
                break

    if not frames:
        return ""

    audio = np.concatenate(frames, axis=0)

    rms = np.sqrt(np.mean((audio.astype(np.float32) * gain) ** 2))
    if rms < 20:
        return ""

    audio_f32 = (audio.astype(np.float32) / 32768.0) * gain  # normalize to [-1,1], apply gain
    peak = float(np.max(np.abs(audio_f32)) + 1e-12)
    if peak > 0.99:
        audio_f32 /= peak / 0.99  # simple limiter

    p = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    sf.write(p, audio_f32, sr, subtype="PCM_16")

    txt = OpenAI().audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        language="en",
        file=open(p, "rb"),
        response_format="text"
    )
    print("User: ", txt)
    print("\n")

    txt = "You are Pico, a helpful AI assistant. Keep your responses concise.\n" + txt
    return txt


# Give model user input and get back model's response
def get_response(text):
    print("Thinking...\n")
    response = client.responses.create(
        model="gpt-4o-mini",
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
    audio += 6  # increase volume

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
