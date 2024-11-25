import requests
import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
from apscheduler.schedulers.background import BackgroundScheduler  # Import the scheduler

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_data.db'  # Update with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api_key = os.getenv("API_KEY")

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
    'West Bengal': 'Kolkata',
}

capitals = list(indian_states_and_capitals.values())

class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    wind_speed = db.Column(db.Float, nullable=False)
    visibility = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

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

def fetch_and_store_weather_data():
    for capital in capitals:
        weather_data = fetch_weather(capital)
        if weather_data[0]:  # If data was fetched successfully
            # Store weather data in the database
            new_record = WeatherData(
                city=weather_data[0],
                country=weather_data[1],
                description=weather_data[4],
                temperature=weather_data[5],
                humidity=weather_data[6],
                wind_speed=weather_data[3],
                visibility=weather_data[2],
                timestamp=datetime.now()
            )
            db.session.add(new_record)
    db.session.commit()  # Commit all new records at once

@app.route('/', methods=['GET', 'POST'])
def select_capital():
    selected_capital = None
    weather_data = None
    
    if request.method == 'POST':
        selected_capital = request.form['capitals']
        if selected_capital:
            weather_data = fetch_weather(selected_capital)
            if weather_data[0]:  # If data was fetched successfully
                # Store weather data in the database
                new_record = WeatherData(
                    city=weather_data[0], 
                    country=weather_data[1],
                    description=weather_data[4],
                    temperature=weather_data[5],
                    humidity=weather_data[6],
                    wind_speed=weather_data[3],
                    visibility=weather_data[2],
                    timestamp=datetime.now()
                )
                db.session.add(new_record)
                db.session.commit()
            
    current_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
    return render_template('sample.html', capitals=capitals, selected_capital=selected_capital, weather_data=weather_data, current_time=current_time)

@app.route('/weather_data', methods=['GET', 'POST'])
def weather_data():
    all_weather_data = {}
    selected_state = None

    if request.method == 'POST':
        selected_state = request.form['state']

    for state, capital in indian_states_and_capitals.items():
        # Fetch weather data for each capital
        weather_records = WeatherData.query.filter_by(city=capital).all()
        all_weather_data[state] = weather_records

    return render_template('weather_data.html', all_weather_data=all_weather_data, selected_state=selected_state, states=list(indian_states_and_capitals.keys()))

# Setting up the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_store_weather_data, 'interval', days=7)  # Fetch every week
scheduler.start()



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run(host='0.0.0.0', port=10000)
