import pico

def main():
    sleep_phrases = ["sleep", "go to sleep", "bye pico"]

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
            
            # Get model response
            model_output = pico.get_response(text)

            # Covert to speech
            pico_audio = pico.text_to_speech(model_output)

            # Play response
            pico.run(text, model_output, pico_audio)