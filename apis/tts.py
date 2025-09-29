from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play
from apis.brain import out
import io

client = OpenAI()

response = client.audio.speech.create(
    model = "gpt-4o-mini-tts",
    voice = "ash",
    input = out
)

audio_bytes = response.read()
audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")