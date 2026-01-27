import wave
from piper import PiperVoice

def convert_text_to_audio(text):
    voice = PiperVoice.load("/home/cole/Pico/piper-voices/en_US-kusal-medium.onnx")
    with wave.open("/home/cole/Pico/audio_files/sound.wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)