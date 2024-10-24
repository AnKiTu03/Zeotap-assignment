
import google.generativeai as genai
import requests
from backend.storage import get_weather_data_for_day
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("api_key")
genai.configure(api_key=api_key)
API_KEY = os.getenv("API_KEY")


# Function to call OpenWeather API and get weather data
def fetch_weather_data_from_openweather(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch weather data: {response.status_code}")
        

# Function to prompt the LLM for a summary
def generate_weather_summary(city_name, selected_date, weather_data_from_db, openweather_data):
    prompt = f"""
    Summarize the weather for {city_name} on {selected_date}.
    
    Weather Data from OpenWeather:
    {openweather_data}

    Additional data from the Firebase:
    {weather_data_from_db}

    Provide a concise three-line summary of the weather.
    """
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 100,
        "response_mime_type": "text/plain",
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-002",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    
    return response.text

def get_weather_summary(city_name, selected_date):
    weather_data_from_db = get_weather_data_for_day(city_name, selected_date)
    openweather_data = fetch_weather_data_from_openweather(city_name)
    weather_summary = generate_weather_summary(city_name, selected_date, weather_data_from_db, openweather_data)
    return weather_summary
