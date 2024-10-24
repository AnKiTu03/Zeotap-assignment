import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px # type: ignore
from streamlit_autorefresh import st_autorefresh # type: ignore
import streamlit_shadcn_ui as ui # type: ignore

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from backend.storage import get_weather_data_for_day
from backend.alert_system import check_thresholds, send_email_alert
from backend.LLMs import get_weather_summary
from backend.processor import collect_weather_data

st.set_page_config(page_title="Weather Monitoring", page_icon="🌦️")

st.markdown("<h1 style='text-align: center;'>🌦️ Real-Time Weather Monitoring</h1>", unsafe_allow_html=True)

st.markdown("---")

if "city_name" not in st.session_state or \
   "temp_threshold" not in st.session_state or \
   "consecutive_threshold" not in st.session_state or \
   "selected_date" not in st.session_state or \
   "temp_unit" not in st.session_state:
    st.error("Please set up your preferences in the Input Page first.")
    st.stop()

city_name = st.session_state['city_name']
temp_threshold = st.session_state['temp_threshold']
consecutive_threshold = st.session_state['consecutive_threshold']
selected_date = st.session_state['selected_date']
temp_unit = st.session_state['temp_unit']  
user_email = st.session_state['user_email']
refresh_interval = 5 * 60 * 1000 


collect_weather_data()


if 'weather_data' not in st.session_state:
    st.session_state['weather_data'] = get_weather_data_for_day(city_name, selected_date)

st_autorefresh(interval=refresh_interval, key="data_refresh")

weather_data = st.session_state['weather_data']

if weather_data:
    try:
        df = pd.DataFrame(weather_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.sort_values('timestamp')

        if temp_unit == 'Kelvin':
            df['temp'] += 273.15
            df['feels_like'] += 273.15
            temp_symbol = 'K'
        else:
            temp_symbol = '°C'

        temps = df['temp'].to_numpy()
        avg_temp = temps.mean()
        max_temp = temps.max()
        min_temp = temps.min()

        if 'main' in df.columns:
            dominant_weather_condition = df['main'].mode()[0]
        else:
            dominant_weather_condition = "Unknown"

        newest_data = df.iloc[-1]
        temp = newest_data['temp']
        feels_like = newest_data['feels_like']

        st.markdown("<h3 style='text-align: center;'>📊 Current Weather Metrics</h3>", unsafe_allow_html=True)
        cols = st.columns(2)
        with cols[0]:
            ui.card(title="Current Weather", content=f"{temp:.2f}{temp_symbol}", key="card1").render()
        with cols[1]:
            ui.card(title="Feels Like", content=f"{feels_like:.2f}{temp_symbol}", key="card2").render()


        with st.spinner("🔍 Generating weather summary..."):
            try:
                weather_summary = get_weather_summary(city_name, selected_date)
                st.subheader(f"📝 Weather Summary for {city_name} on {selected_date}")
                st.info(weather_summary)
            except Exception as e:
                st.error(f"Failed to generate weather summary: {e}")

        st.markdown("<h3 style='text-align: center;'>📈 Temperature Statistics</h3>", unsafe_allow_html=True)
        cols = st.columns(3)
        with cols[0]:
            st.metric("🌡️ Avg Temp", f"{avg_temp:.2f}{temp_symbol}")
        with cols[1]:
            st.metric("🌡️ Max Temp", f"{max_temp:.2f}{temp_symbol}")
        with cols[2]:
            st.metric("🌡️ Min Temp", f"{min_temp:.2f}{temp_symbol}")

        cols = st.columns(4)
        with cols[0]:
            ui.card(title="Avg", content=f"{avg_temp:.2f}{temp_symbol}", key="card3").render()
        with cols[1]:
            ui.card(title="Max", content=f"{max_temp:.2f}{temp_symbol}", key="card4").render()
        with cols[2]:
            ui.card(title="Min", content=f"{min_temp:.2f}{temp_symbol}", key="card5").render()
        with cols[3]:
            ui.card(title="Condition", content=dominant_weather_condition, key="card6").render()
        
        st.markdown("<h3 style='text-align: center;'>📅 Temperature Changes Over Time</h3>", unsafe_allow_html=True)

        if 'temp' in df.columns:
            fig = px.line(df, x='timestamp', y='temp', title=f'Temperature Changes Over Time in {city_name}',
                          labels={'temp': f'Temperature ({temp_symbol})', 'timestamp': 'Time'},
                          markers=True)
            
            fig.update_layout(
                xaxis_title="Time",
                yaxis_title=f'Temperature ({temp_symbol})',
                template='plotly_white',
                hovermode="x unified",
                title_x=0.5,
                xaxis=dict(
                    showgrid=False,
                    tickformat='%H:%M',
                ),
                yaxis=dict(showgrid=True)
            )
            
            fig.add_annotation(
                x=df['timestamp'][df['temp'].idxmax()],
                y=max_temp,
                text=f"Max Temp: {max_temp:.2f}{temp_symbol}",
                showarrow=True,
                arrowhead=1,
                ax=-40,
                ay=-40,
                bgcolor="rgba(255,0,0,0.2)"
            )
            fig.add_annotation(
                x=df['timestamp'][df['temp'].idxmin()],
                y=min_temp,
                text=f"Min Temp: {min_temp:.2f}{temp_symbol}",
                showarrow=True,
                arrowhead=1,
                ax=-40,
                ay=40,
                bgcolor="rgba(0,255,0,0.2)"
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No temperature data available to plot.")

        if check_thresholds(city_name, temp, temp_threshold, consecutive_threshold):
            st.error(f"⚠️ ALERT: {city_name} temperature exceeded {temp_threshold}°{temp_symbol}!")
            send_email_alert(city_name, temp, user_email)
        else:
            st.write(f"✅ No alerts for {city_name}. Current temperature: {temp:.2f}{temp_symbol}.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.warning("No weather data available.")
