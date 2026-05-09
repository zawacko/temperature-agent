import requests
import streamlit as st

st.title("Temperature Dashboard 🌡️")

url = "https://api.open-meteo.com/v1/forecast?latitude=37.3&longitude=-121.9&current_weather=true"

response = requests.get(url)
data = response.json()

current_temp = data["current_weather"]["temperature"]
wind_speed = data["current_weather"]["windspeed"]
time = data["current_weather"]["time"]

st.metric("Current Temperature", f"{current_temp} °C")
st.metric("Wind Speed", f"{wind_speed} km/h")
st.write("Last updated:", time)

history = [12, 14, 15, current_temp]

st.subheader("Temperature History")
st.line_chart(history)

previous = history[-2]
max_temp = max(history[:-1])

st.subheader("Agent Decision")

if current_temp > previous:
    st.success("Temperature increased")
elif current_temp < previous:
    st.warning("Temperature decreased")
else:
    st.info("Temperature stayed the same")

if current_temp > max_temp:
    st.error("New record temperature!")
else:
    st.write("No new record.")
