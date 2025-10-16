import requests

# Get's cities current temperature
def get_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    # search url using requests
    response = requests.get(url, params={
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    })
    # extract current weather data from json
    data = response.json()["current_weather"]

    # get temperature
    temperature = data["temperature"]
    # convert to farenheit
    temperature = int(temperature * 9/5 + 32)

    return temperature