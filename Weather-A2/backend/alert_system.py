import time
from datetime import datetime
from backend.storage import get_weather_data_for_day
import yagmail  # type: ignore
import os
from dotenv import load_dotenv # type: ignore
load_dotenv()

your_email = 'ankitupatil123@gmail.com'
your_password = os.getenv("your_password")
yag = yagmail.SMTP(user=your_email, password=your_password)

thresholds = {
    "Bangalore": {"temp_threshold": 19, "consecutive_count": 1},
    "Mumbai": {"temp_threshold": 36, "consecutive_count": 1},
    "Chennai": {"temp_threshold": 34, "consecutive_count": 1},
    "Kolkata": {"temp_threshold": 37, "consecutive_count": 1},
    "Hyderabad": {"temp_threshold": 35, "consecutive_count": 1},
    "Delhi": {"temp_threshold": 40, "consecutive_count": 1},
}
consecutive_count = {city: 0 for city in thresholds}

last_email_sent_time = {city: 0 for city in thresholds}

def check_thresholds(city, temp, temp_threshold, consecutive_threshold, cooldown_period=1800):
    if temp > temp_threshold:
        consecutive_count[city] += 1
    else:
        consecutive_count[city] = 0

    if consecutive_count[city] >= consecutive_threshold:
        current_time = time.time()
        if current_time - last_email_sent_time[city] >= cooldown_period:
            last_email_sent_time[city] = current_time
            return True
    
    return False


def send_email_alert(city, temp, email):
    recipient_email = email
    subject = f"Weather Alert for {city}"
    body = f"The temperature in {city} has exceeded the threshold: {temp}°C."

    try:
        yag.send(to=recipient_email, subject=subject, contents=body)
        print(f"Email alert successfully sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def collect_and_check_weather(city_name, selected_date):

    weather_data = get_weather_data_for_day(city_name, selected_date)

    if not weather_data:
        print(f"No weather data available for {city_name} on {selected_date}.")
        return

    for weather_info in weather_data:
        temp = weather_info.get('temp') 
        if temp is None:
            print(f"Temperature data is missing for {city_name} on {selected_date}.")
            continue

        if check_thresholds(city_name, temp):
            print(f"ALERT: {city_name} temperature exceeded {thresholds[city_name]['temp_threshold']}°C for {consecutive_count[city_name]} consecutive updates.")
            send_email_alert(city_name, temp)

def continuous_weather_check(city_name):
    """
    Continuously check the weather data for a city at regular intervals (e.g., every 5 minutes).
    """
    while True:
        selected_date = datetime.now().date()
        collect_and_check_weather(city_name, selected_date)

        time.sleep(300)

if __name__ == "__main__":
    selected_city = "Bangalore"
    continuous_weather_check(selected_city)
