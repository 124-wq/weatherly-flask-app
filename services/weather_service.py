import requests
import os
from datetime import datetime

API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()


    lat = data["coord"]["lat"]
    lon = data["coord"]["lon"]

    map_link = f"https://www.google.com/maps?q={lat},{lon}"

    
    weather = {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "feels_like": data["main"]["feels_like"],
        "pressure": data["main"]["pressure"],
        "latitude": lat,
        "longitude": lon,
        "map_link": map_link,
        "updated": datetime.now().strftime("%d %b %Y, %I:%M %p")
    }

    return weather