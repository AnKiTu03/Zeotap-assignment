import requests
from datetime import datetime
import sys
import os
from dotenv import load_dotenv  # type: ignore
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.storage import add_weather_data

load_dotenv()
API_KEY = os.getenv('API_KEY')

def fetch_weather(city_name):
    """
    Fetches weather data for a given city using OpenWeatherMap API.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    # Process the current weather data
    current_weather = {
        "city": f"{datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')}-{city_name}",
        "main": data['weather'][0]['main'],  
        "temp": data['main']['temp'] - 273.15, 
        "feels_like": data['main']['feels_like'] - 273.15,  
        "timestamp": datetime.fromtimestamp(data['dt'])
    }
    
    return current_weather

def main(city_name):
    city = city_name
    weather_info = fetch_weather(city)
    add_weather_data(weather_info)
    return weather_info

if __name__ == "__main__":
    main()



