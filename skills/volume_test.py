import sounddevice as sd
import numpy as np

samplerate = 16000
block_size = 1024

with sd.InputStream(samplerate=samplerate, channels=1) as stream:
    while True:
        block, _ = stream.read(block_size)
        volume = np.linalg.norm(block)
        print(volume)