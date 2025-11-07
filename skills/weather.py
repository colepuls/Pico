import requests

def get_weather(lat, lon):
    """
    This function simply gets the current weather using a url search.
    """

    url = "https://api.open-meteo.com/v1/forecast"
    
    # Search url using requests
    response = requests.get(url, params={
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    })
    
    data = response.json()["current_weather"] # extract current weather data from json
    
    temperature = data["temperature"] # get temperature
    
    temperature = int(temperature * 9/5 + 32) # convert to farenheit

    return temperature