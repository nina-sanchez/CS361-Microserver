from flask import Flask, jsonify
import requests

app = Flask(__name__)

# weather API from our conversation 
weather_key = "7168de5d405a4ab7b7903157232807" # the key from the weather api
weather_base_url = "https://api.weatherapi.com/v1/forecast.json"

# fetches weather data
def fetch_weather_data(location):
    params = {
        "key": weather_key,
        "q": location,
        "days": 1,  # only gets forecast for that day
    }
    response = requests.get(weather_base_url, params=params)
    return response.json()

# will send information to text file, weather api sends in celsius so it's converted here
def update_weather_in_file(file_path, location, high_temp_c, low_temp_c, precip_chance):
    high_temp_f = (high_temp_c * 9/5) + 32
    low_temp_f = (low_temp_c * 9/5) + 32

    with open(file_path, 'w') as file:
        file.write(f"Location: {location}\n")
        file.write(f"High Temp: {high_temp_f:.2f}°F\n")  # will ensure temp is at most two decimals
        file.write(f"Low Temp: {low_temp_f:.2f}°F\n")
        file.write(f"Precipitation Chance: {precip_chance}%\n")

# will fetch and update forecast data in text file
@app.route('/update_forecast', methods=['POST'])
def update_forecast():
    file_path = 'weather_data.txt'  # path to text file

    # can read zip code or city name
    with open(file_path, 'r') as file:
        location = file.readline().strip()

    weather_data = fetch_weather_data(location)

    forecast = weather_data['forecast']['forecastday'][0]['day']
    high_temp = forecast['maxtemp_c']
    low_temp = forecast['mintemp_c']
    precip_chance = forecast['daily_chance_of_rain']

    # returns weather information to text file
    update_weather_in_file(file_path, location, high_temp, low_temp, precip_chance)

    return jsonify({'message': 'weather info updated'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
