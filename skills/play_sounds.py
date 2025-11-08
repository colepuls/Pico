import sounddevice as sd, soundfile as sf
import numpy as np

def play_sound(path):
    data, samplerate = sf.read(f"{path}", dtype='float32')

    volume = 5 # tweak volume

    data = np.clip(data * volume, -1.0, 1.0) # stabalize
    
    sd.play(data, samplerate) # play audio

    sd.wait()