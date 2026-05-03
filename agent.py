import requests

url = "https://api.open-meteo.com/v1/forecast?latitude=37.3&longitude=-121.9&current_weather=true"

response = requests.get(url)

data = response.json()

print(data)
