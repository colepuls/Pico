from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play
import io

client = OpenAI()

response = client.audio.speech.create(
    model = "gpt-4o-mini-tts",
    voice = "ash",
    input = "Hello, i'm Pico, your friendly AI assistant."
)

audio_bytes = response.read()
audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
play(audio)