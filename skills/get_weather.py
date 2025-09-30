import requests

def get_weather(lat=38.95, lon=-92.33):  # Columbia, MO
    url = "https://api.open-meteo.com/v1/forecast"
    r = requests.get(url, params={"latitude": lat, "longitude": lon, "current_weather": True})
    data = r.json()["current_weather"]

    temp = data["temperature"]
    temp_f = int(temp * 9/5 + 32)  # Convert to Fahrenheit
    code = data["weathercode"]

    conditions = {
        0: "Clear skies",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Foggy",
        51: "Light drizzle",
        61: "Rain",
        63: "Heavy rain",
        71: "Snow",
        80: "Rain showers",
        95: "Thunderstorm",
    }
    cond = conditions.get(code, "Unknown")

    return f"The current weather is {temp_f} degrees and {cond}."
