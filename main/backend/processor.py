import schedule
import time
from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.data_fetcher import fetch_weather
from backend.storage import add_weather_data

cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]

def collect_weather_data():
    """
    Fetch and store weather data for all cities.
    """
    print(f"Collecting weather data at {datetime.now()}")
    for city in cities:
        weather_info = fetch_weather(city)
        add_weather_data(weather_info)

# Schedule to run every 5 minutes
schedule.every(5).minutes.do(collect_weather_data)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
