import sounddevice as sd, soundfile as sf
import numpy as np
from skills.samplerate_conversion import resample

def play_sound(path):
    data, samplerate = sf.read(f"{path}", dtype='float32')

    resampled_data = resample(data, samplerate, 48000)

    volume = 3 # tweak volume

    #data = np.clip(data * volume, -1.0, 1.0) # stabalize

    resampled_data = np.clip(resampled_data * volume, -1.0, 1.0)
    
    #sd.play(data, samplerate)

    sd.play(resampled_data, 48000)

    sd.wait()