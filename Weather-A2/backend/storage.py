import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta

cred = credentials.Certificate('/home/Zeotap/main/config/zeotap-dddc1-firebase-adminsdk-hvf95-0a5785de5c.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def add_weather_data(weather_data):

    city_name = weather_data['city'].split('-')[-1]
    city_collection = db.collection(city_name)

    doc_ref = city_collection.document(weather_data['timestamp'].isoformat())
    doc_ref.set(weather_data)
    
    print(f"Weather data for {weather_data['city']} added to Firebase collection '{city_name}'")

def get_weather_data_for_day(city_name, selected_date):

    start_datetime = datetime.combine(selected_date, datetime.min.time())
    end_datetime = datetime.combine(selected_date + timedelta(days=1), datetime.min.time())
    docs = db.collection(city_name)\
        .where('timestamp', '>=', start_datetime)\
        .where('timestamp', '<', end_datetime)\
        .stream()
    
    weather_data_selected_date = []
    for doc in docs:
        data = doc.to_dict()
        weather_data_selected_date.append(data)
    
    return weather_data_selected_date