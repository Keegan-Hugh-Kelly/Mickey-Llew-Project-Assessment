import requests
import folium
from flask import Flask, render_template, Response, request, redirect, url_for
import os
import datetime
from jinja2 import Undefined
import pandas as pd
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact_messages.db'
db = SQLAlchemy(app)

API_KEY = 'c15281beae1e4915fef587ae1b1382ce'  # Change to your API key
API_KEY_NAME = 'default'  # Change to your API key name
CITY = 'Cape Town'  # Default city
UNITS = 'metric'  # Change to 'imperial' for Fahrenheit

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    try:
        weather_data = get_weather_data()
        weather_forecast = get_weather_forecast()

        return render_template(
            'index.html',
            weather_data=weather_data,
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


@app.route('/search', methods=['GET'])
def search():
    global CITY
    query = request.args.get('query')
    CITY = query if query else 'Cape Town'

    referrer = request.referrer
    if referrer and 'weather-map' in referrer:
        return redirect(url_for('weather_map'))
    elif referrer and 'weather-graph' in referrer:
        return redirect(url_for('weather_graphs'))
    elif referrer and 'weather-table' in referrer:
        return redirect(url_for('weather_tables'))
    else:
        return redirect(url_for('index'))

@app.route('/weather-map')
def weather_map():
    try:
        weather_data = get_weather_data()
        return render_template('weather_map.html', weather_data=weather_data, city=CITY)
    except Exception as e:
        error_message = f"Error: {e}"
        return render_template('error.html', error_message=error_message)

@app.route('/weather-graphs')
def weather_graphs():
    try:
        weather_forecast = get_weather_forecast()

        dates = [forecast['date'] for forecast in weather_forecast]
        max_temperatures = [forecast['temperature_max']
                            for forecast in weather_forecast]
        min_temperatures = [forecast['temperature_min']
                            for forecast in weather_forecast]
        precipitations = [forecast['precipitation']
                          for forecast in weather_forecast]
        wind_speeds = [forecast['wind_speed'] for forecast in weather_forecast]
        wind_directions = [forecast['wind_direction']
                           for forecast in weather_forecast]
        humidities = [forecast['humidity'] for forecast in weather_forecast]
        uv_indices = [forecast['uv_index'] for forecast in weather_forecast]

        dates = [date if date is not Undefined else None for date in dates]
        max_temperatures = [
            temp if temp is not Undefined else None for temp in max_temperatures]
        min_temperatures = [
            temp if temp is not Undefined else None for temp in min_temperatures]
        precipitations = [
            precip if precip is not Undefined else None for precip in precipitations]
        wind_speeds = [
            speed if speed is not Undefined else None for speed in wind_speeds]
        wind_directions = [
            direction if direction is not Undefined else None for direction in wind_directions]
        humidities = [
            humidity if humidity is not Undefined else None for humidity in humidities]
        uv_indices = [uv if uv is not Undefined else None for uv in uv_indices]

        return render_template(
            'weather_graphs.html',
            dates=dates,
            max_temperatures=max_temperatures,
            min_temperatures=min_temperatures,
            precipitations=precipitations,
            wind_speeds=wind_speeds,
            wind_directions=wind_directions,
            humidities=humidities,
            uv_indices=uv_indices,
            city=CITY
        )

    except Exception as e:
        error_message = f"Error: {e}"
        return render_template('error.html', error_message=error_message)
    
@app.route('/weather-tables')
def weather_tables():
    try:
        weather_forecast = get_weather_forecast()

        return render_template(
            'weather_tables.html',
            weather_forecast=weather_forecast,
            city=CITY
        )
    except Exception as e:
        error_message = f"Error: {e}"
        return render_template('error.html', error_message=error_message)
    
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form['email']
        message = request.form['message']
        contact_message = ContactMessage(email=email, message=message)
        db.session.add(contact_message)
        db.session.commit()
        return redirect(url_for('contact'))

    return render_template('contact.html')
    
def degrees_to_compass(degrees):
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(degrees / 22.5) % 16
    return directions[index]

def get_weather_forecast():
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={CITY}&units={UNITS}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if 'list' not in data:
        raise Exception(
            f"Unable to retrieve weather forecast data. Response: {data}")

    weather_forecast = []

    for item in data['list']:
        date_time = datetime.datetime.fromtimestamp(item['dt'])
        date = date_time.date()
        wind_direction_deg = item['wind']['deg']
        wind_direction = degrees_to_compass(wind_direction_deg)

        for forecast in weather_forecast:
            if forecast['date'] == date:
                temperature = item['main']['temp']
                description = item['weather'][0]['description']
                precipitation = 0.0

                if 'rain' in item and '3h' in item['rain']:
                    precipitation += item['rain']['3h']
                if 'snow' in item and '3h' in item['snow']:
                    precipitation += item['snow']['3h']

                forecast['temperature_max'] = max(
                    forecast['temperature_max'], temperature)
                forecast['temperature_min'] = min(
                    forecast['temperature_min'], temperature)
                forecast['description'] = description
                forecast['precipitation'] += precipitation
                forecast['wind_speed'] = item['wind']['speed']
                forecast['wind_direction'] = wind_direction
                forecast['humidity'] = item['main']['humidity']
                forecast['uv_index'] = None
                forecast['cloud_coverage'] = item['clouds']['all']
                break
        else:
            day_name = date.strftime('%A')
            temperature = item['main']['temp']
            description = item['weather'][0]['description']
            precipitation = 0.0

            if 'rain' in item and '3h' in item['rain']:
                precipitation += item['rain']['3h']
            if 'snow' in item and '3h' in item['snow']:
                precipitation += item['snow']['3h']

            weather_forecast.append({
                'date': date,
                'day_name': day_name,
                'temperature_max': temperature,
                'temperature_min': temperature,
                'description': description,
                'precipitation': precipitation,
                'cloud_coverage': item['clouds']['all'],
                'wind_speed': item['wind']['speed'],
                'wind_direction': wind_direction,
                'humidity': item['main']['humidity'],
                'uv_index': None,
                'graphic_url': get_cloud_coverage_graphic(description)
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
