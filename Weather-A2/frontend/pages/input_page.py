import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import datetime

st.set_page_config(page_title="Setup Weather Alerts", page_icon="🌦️")

st.title('⚙️ Setup Weather Alerts')

st.markdown("""
### 🌤️ Configure your preferences to receive weather alerts.
Fill out the form below to set up weather monitoring for your selected city and conditions.
""")

if 'user_email' not in st.session_state:
    st.session_state['user_email'] = ''

if 'city_name' not in st.session_state:
    st.session_state['city_name'] = 'Delhi'

if 'temp_threshold' not in st.session_state:
    st.session_state['temp_threshold'] = 35

if 'consecutive_threshold' not in st.session_state:
    st.session_state['consecutive_threshold'] = 2

if 'selected_date' not in st.session_state:
    st.session_state['selected_date'] = datetime.date.today()

if 'temp_unit' not in st.session_state:
    st.session_state['temp_unit'] = 'Celsius' 

user_email = st.text_input("📧 Enter your Email:", value=st.session_state['user_email'])

city_list = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
city_name = st.selectbox("🏙️ Select a City:", city_list, index=city_list.index(st.session_state['city_name']))

temp_threshold = st.slider(f"🌡️ Set Temperature Threshold for {city_name} (°C):", 
                           min_value=18, max_value=35, value=st.session_state['temp_threshold'])

consecutive_threshold = st.number_input("🔄 Set Consecutive Updates Threshold:", 
                                        min_value=1, max_value=10, value=st.session_state['consecutive_threshold'])

selected_date = st.date_input("📅 Select a Date:", value=st.session_state['selected_date'], max_value=datetime.date.today())

temp_unit = st.radio("🌡️ Select Temperature Unit:", ('Celsius', 'Kelvin'), index=0 if st.session_state['temp_unit'] == 'Celsius' else 1)

st.markdown("---")

if st.button("💾 Save Preferences"):
    st.session_state['user_email'] = user_email
    st.session_state['city_name'] = city_name
    st.session_state['temp_threshold'] = temp_threshold
    st.session_state['consecutive_threshold'] = consecutive_threshold
    st.session_state['selected_date'] = selected_date
    st.session_state['temp_unit'] = temp_unit

    st.success("✅ Your preferences have been saved!")

    switch_page("Weather page")
