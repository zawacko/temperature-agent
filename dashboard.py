import streamlit as st
import requests
import json
from streamlit_autorefresh import st_autorefresh

# 🔁 Auto refresh every hour (3600 seconds)
st_autorefresh(interval=3600 * 1000, key="refresh")

st.title("🌡️ Temperature Dashboard")

HISTORY_FILE = "history.json"

# Load history
try:
    with open(HISTORY_FILE, "r") as file:
        history = json.load(file)
except:
    history = []

# Get live data
url = "https://api.open-meteo.com/v1/forecast?latitude=37.3&longitude=-121.9&current_weather=true"
response = requests.get(url)
data = response.json()

current_temp = data["current_weather"]["temperature"]
wind_speed = data["current_weather"]["windspeed"]
time = data["current_weather"]["time"]

# Save to history
history.append({
    "time": time,
    "temperature": current_temp
})

with open(HISTORY_FILE, "w") as file:
    json.dump(history, file, indent=4)

# Display current data
st.metric("Current Temperature (°C)", current_temp)
st.metric("Wind Speed (km/h)", wind_speed)
st.write("Last updated:", time)

# Graph
temps = [item["temperature"] for item in history]

st.subheader("📈 Temperature History")
st.line_chart(temps)

# Agent logic
if len(history) > 1:
    previous = history[-2]["temperature"]
    max_temp = max(item["temperature"] for item in history[:-1])
else:
    previous = current_temp
    max_temp = current_temp

st.subheader("🤖 Agent Decision")

if current_temp > previous:
    st.success("Temperature increased")
elif current_temp < previous:
    st.warning("Temperature decreased")
else:
    st.info("Temperature stayed the same")

if current_temp > max_temp and len(history) > 1:
    st.error("🚨 New record temperature!")
else:
    st.write("No new record.")
