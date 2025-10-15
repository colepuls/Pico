import sounddevice as sd
import soundfile as sf
import numpy as np
import wave
from piper import PiperVoice

def speak(text):
    # generate sound file
    voice = PiperVoice.load("/home/colecodes/projects/Pico/piper-voices/en_US-kusal-medium.onnx")
    with wave.open("sound.wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

    # play sound file through speaker
    data, samplerate = sf.read("sound.wav", dtype='float32')

    # tweak speaker volume
    volume = 4
    data = np.clip(data * volume, -1.0, 1.0) # stabalize
    
    sd.play(data, samplerate)
    sd.wait()  # wait for audio to finish
