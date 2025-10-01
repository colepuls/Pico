import re
import pico
import skills.get_weather as gw
import skills.alarms as alarms

def main():
    weather_phrases = ["weather", "forecast", "temperature"]
    alarm_phrases = ["set an alarm", "alarm for"]
    weather_text = ""
    alarm_text = ""

    while True:
        if pico.awake is False:
            pico.wait_for_wake()
        else:
            text = pico.speech_to_text()
            if not text:
                continue
            low = text.lower()

            # Weather
            if any(p in low for p in weather_phrases):
                weather_text = gw.get_weather(lat=38.95, lon=-92.33)
                pico_audio = pico.text_to_speech(weather_text)
                pico.run(text, weather_text, pico_audio)
                pico.awake = False
                continue

            # Alarm: extract 12h time like "9:30 PM"
            if any(p in low for p in alarm_phrases):
                time_str = alarms.extract_time_12h(text)
                if time_str:
                    target = alarms.set_alarm(time_str)  # non-blocking
                    say = f"Alarm set for {target.strftime('%Y-%m-%d %I:%M %p')}"
                else:
                    say = "I didn't catch the time. Say something like 'set an alarm for 6:45 AM'."

                pico_audio = pico.text_to_speech(say)
                pico.run(text, say, pico_audio)
                pico.awake = False
                continue

            # Fallback model response
            model_output = pico.get_response(text)
            pico_audio = pico.text_to_speech(model_output)
            pico.run(text, model_output, pico_audio)
            pico.awake = False
