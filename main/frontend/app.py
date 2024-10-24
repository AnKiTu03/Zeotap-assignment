import streamlit as st

st.set_page_config(page_title= "Weather Dashboard", page_icon=":cloud:")
st.title("🌦️Main Dashboard")
st.write(" ", divider=True)
st.write("### How to use this :blue[dashboard]:", divider=True)
st.write("- Use the **sidebar** to navigate between different sections of the app.")
st.write("- Access **real-time weather monitoring**, **data visualizations**, and **reports**.")
st.write("- Set up your **preferences** for alerts and weather conditions.")
st.markdown("<p style='text-align: center;'>🌦️ Stay updated with the latest insights!</p>", unsafe_allow_html=True)
st.info("Use the **menu on the left** to explore different pages and get insights.")

