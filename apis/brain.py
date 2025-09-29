from openai import OpenAI
from apis import stt

client = OpenAI()
prompt = stt.txt

response = client.responses.create(
    model="gpt-4o-mini",
    input = prompt
)

out = response.output_text