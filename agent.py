import requests
import os
import smtplib
from email.message import EmailMessage

print("Starting agent...")

# API request
url = "https://api.open-meteo.com/v1/forecast?latitude=37.3&longitude=-121.9&current_weather=true"
response = requests.get(url)
data = response.json()

# Get current temperature
current_temp = data["current_weather"]["temperature"]

# Simulated history (last values + current)
history = [5, 6, 7, current_temp]

# Extract values
current = history[-1]
previous = history[-2]
max_temp = max(history[:-1])  # IMPORTANT FIX

# Print values
print("Current:", current)
print("Previous:", previous)
print("Max:", max_temp)

# Email function (SAFE)
def send_email(message):
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")

    if not email_user or not email_pass:
        print("Email not sent: EMAIL_USER or EMAIL_PASS is missing.")
        return

    email = EmailMessage()
    email.set_content(message)
    email["Subject"] = "Weather Alert"
    email["From"] = email_user
    email["To"] = email_user

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_user, email_pass)
        smtp.send_message(email)

# Agent logic
if current > previous:
    print("Temperature increased")

if current < previous:
    print("Temperature decreased")

if current == previous:
    print("Temperature stayed the same")

if current > max_temp:
    print("New record temperature!")
    send_email(f"New record temperature: {current}")
