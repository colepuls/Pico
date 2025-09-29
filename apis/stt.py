from openai import OpenAI
import sounddevice as sd
import soundfile as sf
import tempfile

sample_rate = 16000
secs = 8

print("Recording...")
audio = sd.rec(int(secs*sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
sd.wait()
p = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
sf.write(p, audio, sample_rate, subtype="PCM_16")
print("Transcribing...")
txt = OpenAI().audio.transcriptions.create(model="gpt-4o-mini-transcribe", file=open(p,"rb"), response_format="text")
print("\n--- Transcript ---\n", txt)
