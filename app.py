import requests
import os
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the API key from environment variables
api_key = os.getenv("API_KEY")

# List of Indian states and their capitals
indian_states_and_capitals = {
    'Andhra Pradesh': 'Amaravati',
    'Arunachal Pradesh': 'Itanagar',
    'Assam': 'Dispur',
    'Bihar': 'Patna',
    'Chhattisgarh': 'Raipur',
    'Goa': 'Panaji',
    'Gujarat': 'Gandhinagar',
    'Haryana': 'Chandigarh',
    'Himachal Pradesh': 'Shimla',
    'Jharkhand': 'Ranchi',
    'Karnataka': 'Bengaluru',
    'Kerala': 'Thiruvananthapuram',
    'Madhya Pradesh': 'Bhopal',
    'Maharashtra': 'Mumbai',
    'Manipur': 'Imphal',
    'Meghalaya': 'Shillong',
    'Mizoram': 'Aizawl',
    'Nagaland': 'Kohima',
    'Odisha': 'Bhubaneswar',
    'Punjab': 'Chandigarh',
    'Rajasthan': 'Jaipur',
    'Sikkim': 'Gangtok',
    'Tamil Nadu': 'Chennai',
    'Telangana': 'Hyderabad',
    'Tripura': 'Agartala',
    'Uttar Pradesh': 'Lucknow',
    'Uttarakhand': 'Dehradun',
    'West Bengal': 'Kolkata'
}

capitals = list(indian_states_and_capitals.values())

def fetch_weather(city_name):
    country_code = "IN"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={api_key}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city = data['name']
        country = data['sys']['country']
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp'] - 273.15
        temperature = format(temperature, ".2f")
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        visibility = data.get('visibility', None)
        return city, country, visibility, wind_speed, weather_description, temperature, humidity
    else:
        return None, None, None, None, None, None, None

@app.route('/', methods=['GET', 'POST'])
def select_capital():
    selected_capital = None
    weather_data = None
    
    if request.method == 'POST':
        selected_capital = request.form['capitals']
        if selected_capital != None:
            weather_data = fetch_weather(selected_capital)
            print(weather_data)
    
    return render_template('sample.html', capitals=capitals, selected_capital=selected_capital, weather_data=weather_data)

if __name__ == '__main__':
      app.run(debug=True, port=10000)
      