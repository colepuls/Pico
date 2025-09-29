from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4o-mini",
    input="Whats the weather right now in Columbia, MO"
)

print(response.output_text)