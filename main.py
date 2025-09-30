import pico
import skills.get_weather as gw

def main():
    sleep_phrases = ["sleep", "go to sleep", "bye pico"]
    weather_phrases = ["weather", "forecast", "temperature"]
    say_weather = False
    weeather_text = ""

    while True:
        if pico.awake == False:
            pico.wait_for_wake()
        elif pico.awake == True:
            # Get user input
            text = pico.speech_to_text()

            if not text:
                continue
            if any(phrase in text.lower() for phrase in sleep_phrases):
                pico.beep()
                pico.awake = False
                continue
            if any(phrase in text.lower() for phrase in weather_phrases):
                weather_text = gw.get_weather(lat=38.95, lon=-92.33)
                pico_audio = pico.text_to_speech(weather_text)
                pico.run(text, weather_text, pico_audio)
                continue

            # Get response
            model_output = pico.get_response(text)

            # Covert to speech
            pico_audio = pico.text_to_speech(model_output)

            # Play response
            pico.run(text, model_output, pico_audio)