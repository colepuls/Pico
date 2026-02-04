from data_stream.samplerate_conversion import resample
import sounddevice as sd
import soundfile as sf
import numpy as np


# Read audio, resample, play
def play_audio(path):
    data, samplerate = sf.read(f"{path}", dtype='float32') 
    
    resampled_data = resample(data, samplerate, 48000)
    volume = 5
    resampled_data = np.clip(resampled_data * volume, -1.0, 1.0)
    
    sd.play(resampled_data, 48000)
    sd.wait()