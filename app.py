import requests

# Replace with your actual API key
api_key = "12a98220f3c74d99ddebd0de42d047a7"

# Replace with the actual city name and country code
city_name = "Kolkata"
country_code = "IN"

# indian_states_and_capitals = {
#     'Andhra Pradesh': 'Amaravati',
#     'Arunachal Pradesh': 'Itanagar',
#     'Assam': 'Dispur',
#     'Bihar': 'Patna',
#     'Chhattisgarh': 'Raipur',
#     'Goa': 'Panaji',
#     'Gujarat': 'Gandhinagar',
#     'Haryana': 'Chandigarh',
#     'Himachal Pradesh': 'Shimla',
#     'Jharkhand': 'Ranchi',
#     'Karnataka': 'Bengaluru',
#     'Kerala': 'Thiruvananthapuram',
#     'Madhya Pradesh': 'Bhopal',
#     'Maharashtra': 'Mumbai',
#     'Manipur': 'Imphal',
#     'Meghalaya': 'Shillong',
#     'Mizoram': 'Aizawl',
#     'Nagaland': 'Kohima',
#     'Odisha': 'Bhubaneswar',
#     'Punjab': 'Chandigarh',
#     'Rajasthan': 'Jaipur',
#     'Sikkim': 'Gangtok',
#     'Tamil Nadu': 'Chennai',
#     'Telangana': 'Hyderabad',
#     'Tripura': 'Agartala',
#     'Uttar Pradesh': 'Lucknow',
#     'Uttarakhand': 'Dehradun',
#     'West Bengal': 'Kolkata'
# }



# API endpoint with parameters
url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={api_key}"

# Make the GET request to the API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON data
    data = response.json()
    # print(data)
    city = data['name']
    country = data['sys']['country']
    weather_description = data['weather'][0]['description']
    temperature = data['main']['temp'] - 273.15
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    visibility = data.get('visibility', None)  # Default to None if visibility is not present
    



    # Print the extracted information
    print(f"City: {city}")
    print(f"Country: {country}")
    print(f"Weather Description: {weather_description}")
    
    if visibility is not None:
        if visibility >= 10000:
            print(f"Visibility is good: {visibility} meters")
        elif 4000 <= visibility < 10000:
            print(f"Visibility is moderate: {visibility} meters")
        else:
            print(f"Visibility is poor: {visibility} meters")

    print(f"Temperature: {temperature}°C")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} m/s")
else:
    print(f"Failed to retrieve data: {response.status_code}")
    print(response.text)  # Print the error message returned by the API
    

print(data)
