import requests
import folium
from flask import Flask, render_template, Response, request, redirect, url_for
import os
import datetime
from jinja2 import Undefined

app = Flask(__name__)

API_KEY = 'c15281beae1e4915fef587ae1b1382ce'  # Change to your API key
API_KEY_NAME = 'default'  # Change to your API key name
CITY = 'Cape Town'  # Default city
UNITS = 'metric'  # Change to 'imperial' for Fahrenheit


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

    # Determine the current page and redirect back to it after the search
    referrer = request.referrer
    if referrer and 'weather-map' in referrer:
        return redirect(url_for('weather_map'))
    elif referrer and 'weather-graph' in referrer:
        return redirect(url_for('weather_graphs'))
    elif referrer and 'weather-table' in referrer:
        return redirect(url_for('weather_tables'))
    else:
        return redirect(url_for('index'))

# Route for the Weather Map page


@app.route('/weather-map')
def weather_map():
    try:
        weather_data = get_weather_data()
        return render_template('weather_map.html', weather_data=weather_data, city=CITY)
    except Exception as e:
        error_message = f"Error: {e}"
        return render_template('error.html', error_message=error_message)

# Route for the Weather Graphs page


@app.route('/weather-graphs')
def weather_graphs():
    try:
        # Get weather forecast data
        weather_forecast = get_weather_forecast()

        # Extracting data for the graphs
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

        # Replace Undefined values with None
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

# Route for the Weather Tables page
@app.route('/weather-tables')
def weather_tables():
    try:
        # Get weather forecast data
        weather_forecast = get_weather_forecast()

        # Create a date range for the next 24 hours, incrementing every 3 hours
        date_range = [datetime.datetime.now() + datetime.timedelta(hours=i) for i in range(0, 24, 3)]

        # Reorganize the weather forecast data by time
        forecast_by_time = {}
        for day_data in weather_forecast:
            date = day_data['date']
            for i, time in enumerate(date_range):
                if time.date() == date.date() and time.hour == date.hour:
                    if time not in forecast_by_time:
                        forecast_by_time[time] = {
                            'temperature_max': day_data['temperature_max'],
                            'temperature_min': day_data['temperature_min'],
                            'description': day_data['description'],
                            'cloud_coverage': day_data['cloud_coverage'],
                            'wind_speed': day_data['wind_speed'],
                            'wind_direction': day_data['wind_direction'],
                            'humidity': day_data['humidity']
                        }
                    else:
                        forecast_by_time[time]['temperature_max'] = max(forecast_by_time[time]['temperature_max'], day_data['temperature_max'])
                        forecast_by_time[time]['temperature_min'] = min(forecast_by_time[time]['temperature_min'], day_data['temperature_min'])

        return render_template('weather_tables.html', city=CITY, forecast_by_time=forecast_by_time, date_range=date_range)

    except Exception as e:
        error_message = f"Error: {e}"
        return render_template('error.html', error_message=error_message)


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
                forecast['wind_direction'] = item['wind']['deg']
                forecast['humidity'] = item['main']['humidity']
                # Placeholder for UV index, as it's not provided by the API
                forecast['uv_index'] = None
                # Add cloud coverage data
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
                # Add cloud coverage data
                'cloud_coverage': item['clouds']['all'],
                'wind_speed': item['wind']['speed'],
                'wind_direction': item['wind']['deg'],
                'humidity': item['main']['humidity'],
                'uv_index': None,  # Placeholder for UV index, as it's not provided by the API
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
