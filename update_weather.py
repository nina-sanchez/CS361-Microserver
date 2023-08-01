import requests

url = 'http://127.0.0.1:5000/update_forecast'
response = requests.post(url)

if response.status_code == 200:
    print("weather data has been updated")
else:
    print(f"status error: {response.status_code}")
