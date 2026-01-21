import sounddevice as sd
import soundfile as sf
import numpy as np
import wave
from skills.samplerate_conversion import resample
from piper import PiperVoice

def speak(text):
    """
    This is a text-to-speech function using the piper model locally.
    - Loads the model and speaks any text passed through it.
    """

    # Generate sound file
    voice = PiperVoice.load("/home/colecodes/projects/Pico/piper-voices/en_US-kusal-medium.onnx")
    with wave.open("/home/colecodes/projects/Pico/audio_files/sound.wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

    # Read sound file
    data, samplerate = sf.read("/home/colecodes/projects/Pico/audio_files/sound.wav", dtype='float32')

    resampled_data = resample(data, samplerate, 48000)

    volume = 3 # tweak volume

    resampled_data = np.clip(resampled_data * volume, -1.0, 1.0)

    #data = np.clip(data * volume, -1.0, 1.0) # stabalize
    
    sd.play(resampled_data, 48000)

    #sd.play(data, samplerate) # play audio
    
    sd.wait() # wait for audio to finish