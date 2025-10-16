import sounddevice as sd
import soundfile as sf
import numpy as np
import wave
from piper import PiperVoice

# ----- TTS Function -----
def speak(text):
    # generate sound file
    voice = PiperVoice.load("/home/colecodes/projects/Pico/piper-voices/en_US-kusal-medium.onnx")
    with wave.open("/home/colecodes/projects/Pico/audio_files/sound.wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

    # play sound file through speaker
    data, samplerate = sf.read("/home/colecodes/projects/Pico/audio_files/sound.wav", dtype='float32')

    # tweak speaker volume
    volume = 7
    # stabalize
    data = np.clip(data * volume, -1.0, 1.0)
    
    sd.play(data, samplerate)
    # wait for audio to finish
    sd.wait()