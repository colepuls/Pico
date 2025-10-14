import sounddevice as sd
import soundfile as sf
import wave
from piper import PiperVoice

def speak(text):
    # generate sound file
    voice = PiperVoice.load("/home/colecodes/projects/Pico/piper-voices/en_US-kusal-medium.onnx")
    with wave.open("sound.wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

    # play sound file through speaker
    data, samplerate = sf.read("sound.wav", dtype='float32')
    sd.play(data, samplerate)
    sd.wait()  # wait for audio to finish
