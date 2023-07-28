import requests
import datetime
import folium
from flask import Flask, render_template, Response
import os
import matplotlib.pyplot as plt

app = Flask(__name__)

API_KEY = 'c15281beae1e4915fef587ae1b1382ce'  # Change to your API key
API_KEY_NAME = 'default'  # Change to your API key name
CITY = 'Cape Town'  # Change to your city
UNITS = 'metric'  # Change to 'imperial' for Fahrenheit

@app.route('/')
def index():
    try:
        weather_data = get_weather_data()
        weather_forecast = get_weather_forecast()

        return render_template(
            'index.html',
            weather_forecast=weather_forecast
        )
    except Exception as e:
        error_message = f"Error: {e}"
        return render_template('error.html', error_message=error_message)

def get_weather_data():
    url = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&units={UNITS}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if 'main' not in data:
        raise Exception(f"Unable to retrieve weather data. Response: {data}")

    return data

# Route for the Weather Map page
@app.route('/weather-map')
def weather_map():
    try:
        weather_data = get_weather_data()
        return render_template('weather_map.html', weather_data=weather_data)
    except Exception as e:
        error_message = f"Error: {e}"
        return render_template('error.html', error_message=error_message)

# Route for the Weather Graphs page
@app.route('/weather-graphs')
def weather_graphs():
    # Add code to generate weather graphs (you can use libraries like matplotlib)

    # For now, just render the template without any data
    return render_template('weather_graphs.html')

# Route for the Weather Tables page
@app.route('/weather-tables')
def weather_tables():
    # Add code to generate weather tables

    # For now, just render the template without any data
    return render_template('weather_tables.html')

def get_weather_forecast():
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={CITY}&units={UNITS}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if 'list' not in data:
        raise Exception(f"Unable to retrieve weather forecast data. Response: {data}")

    weather_forecast = []

    for item in data['list']:
        date_time = datetime.datetime.fromtimestamp(item['dt'])
        date = date_time.date()

        for forecast in weather_forecast:
            if forecast['date'] == date:
                temperature = item['main']['temp']
                description = item['weather'][0]['description']

                forecast['temperature_max'] = max(forecast['temperature_max'], temperature)
                forecast['temperature_min'] = min(forecast['temperature_min'], temperature)
                forecast['description'] = description
                break
        else:
            day_name = date.strftime('%A')
            temperature = item['main']['temp']
            description = item['weather'][0]['description']
            cloud_coverage = item['clouds']['all']
            graphic_url = get_cloud_coverage_graphic(description)

            weather_forecast.append({
                'date': date,
                'day_name': day_name,
                'temperature_max': temperature,
                'temperature_min': temperature,
                'description': description,
                'cloud_coverage': cloud_coverage,
                'graphic_url': graphic_url
            })

    return weather_forecast


def get_cloud_coverage_graphic(description):
    description_lower = description.lower()
    
    if 'clear' in description_lower or 'sun' in description_lower:
        return os.path.join('/static/weatherimages', 'clear.png')
    elif 'cloud' in description_lower:
        return os.path.join('/static/weatherimages', 'cloudy.png')
    
    elif 'overcast' in description_lower:
        return os.path.join('/static/weatherimages', 'partly-cloudy.png')
    
    elif 'rain' in description_lower or 'shower' in description_lower:
        return os.path.join('/static/weatherimages', 'lightrain.png')
    
    elif 'rain' in description_lower or 'shower' in description_lower:
        return os.path.join('/static/weatherimages', 'heavyrain.png')
    
    elif 'thunderstorm' in description_lower:
        return os.path.join('/static/weatherimages', 'thunderstorm.png')
    
    elif 'snow' in description_lower or 'flurry' in description_lower:
        return os.path.join('/static/weatherimages', 'snow.png')
    
    elif 'mist' in description_lower or 'fog' in description_lower:
        return os.path.join('/static/weatherimages', 'mist.png')
    
    else:
        return os.path.join('/static/weatherimages', 'default.png')

if __name__ == '__main__':
    app.run(debug=True)
