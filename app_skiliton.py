
#!/home/zero/miniconda3/envs/WeatherApp/bin/python

import requests
import os


api_key = os.getenv("API_KEY") 


city_name = "San Francisco"
country_code = "US"

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
        print("",city,"\n", country,"\n",weather_description,"\n",temperature,"\n",humidity,"\n",wind_speed,"\n",visibility,"\n")
        print(data)
else:
    print(f"Failed to retrieve data: {response.status_code}")
    print(response.text)  
