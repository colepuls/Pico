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
        "current_weather": True,
        "daily": "temperature_2m_max,temperature_2m_min,weathercode",
        "timezone": "auto"
    })
    
    data = response.json()
    
    # Temperature data
    current_temperature = round(data["current_weather"]["temperature"] * 9/5 + 32)
    daily_high = round(data["daily"]["temperature_2m_max"][0] * 9/5 + 32)
    daily_low = round(data["daily"]["temperature_2m_min"][0] * 9/5 + 32)

    # Condition data
    weather_code = data["daily"]["weathercode"][0]

    WEATHER_CODES = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }

    codition = WEATHER_CODES.get(weather_code)

    return f"""
    The current weather is {current_temperature} degrees fahrenheit.
    Today's low is {daily_low} degrees and the high is {daily_high} degrees.
    The conditions are {codition}.
    """