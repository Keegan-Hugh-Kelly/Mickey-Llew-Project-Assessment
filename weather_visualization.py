import requests
import datetime
import folium
from flask import Flask, render_template
import os

app = Flask(__name__)

API_KEY = 'c15281beae1e4915fef587ae1b1382ce'  # Change to your API key
API_KEY_NAME = 'default'  # Change to your API key name
CITY = 'Cape Town'  # Change to your city
UNITS = 'metric'  # Change to 'imperial' for Fahrenheit

@app.route('/')
def index():
    try:
        weather_data = get_weather_data()
        map_html = display_temperature_on_map(weather_data)
        weather_forecast = get_weather_forecast()

        return render_template(
            'index.html',
            map_html=map_html,
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

def display_temperature_on_map(weather_data):
    lat = weather_data['coord']['lat']
    lon = weather_data['coord']['lon']
    temperature = weather_data['main']['temp']
    CITY = weather_data['name']

    # Create the base map with the 'Default' tiles (OpenStreetMap)
    map_city = folium.Map(location=[lat, lon], zoom_start=10, tiles='OpenStreetMap')

    # Add a tooltip to show temperature by the mouse cursor
    tooltip = f'Temperature: {temperature}°C'
    folium.Marker([lat, lon], popup=f'{CITY}\nTemperature: {temperature}°C', tooltip=tooltip).add_to(map_city)

    # Add 'Satellite' tiles using the default tile source
    folium.TileLayer(tiles='Stamen Terrain', name='Terrain').add_to(map_city)

    # Create a LayerControl for map type with 'Default' (OpenStreetMap) and 'Terrain' (Stamen Terrain) options
    map_layer_control = folium.LayerControl(position='topright', collapsed=False)
    map_city.add_child(map_layer_control)

    # Save the map as an HTML string
    map_html = map_city.get_root().render()

    return map_html

def get_weather_forecast():
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={CITY}&units={UNITS}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if 'list' not in data:
        raise Exception(f"Unable to retrieve weather forecast data. Response: {data}")

    # Filter the data to get weather details for the next two weeks
    today = datetime.date.today()
    two_weeks_later = today + datetime.timedelta(days=14)
    filtered_data = [item for item in data['list'] if today <= datetime.datetime.fromtimestamp(item['dt']).date() <= two_weeks_later]

    # Create a list to store forecast data with cloud coverage graphics
    weather_forecast = []

    for item in filtered_data:
        date_time = datetime.datetime.fromtimestamp(item['dt'])
        date = date_time.date()
        time = date_time.time()
        temperature = item['main']['temp']
        description = item['weather'][0]['description']

        # Get the cloud coverage percentage and corresponding graphic URL
        cloud_coverage = item['clouds']['all']
        graphic_url = get_cloud_coverage_graphic(cloud_coverage)

        weather_forecast.append({
            'date': date,
            'time': time,
            'temperature': temperature,
            'description': description,
            'cloud_coverage': cloud_coverage,
            'graphic_url': graphic_url
        })

    return weather_forecast

def get_cloud_coverage_graphic(cloud_coverage):
    if cloud_coverage < 30:
        return os.path.join('/static/weatherimages', 'clear.png')
    elif 30 <= cloud_coverage < 70:
        return os.path.join('/static/weatherimages', 'partly-cloudy.png')
    elif 70 <= cloud_coverage < 90:
        return os.path.join('/static/weatherimages', 'cloudy.png')
    elif 90 <= cloud_coverage < 95:
        return os.path.join('/static/weatherimages', 'lightrain.png')
    elif 95 <= cloud_coverage < 100:
        return os.path.join('/static/weatherimages', 'heavyrain.png')
    else:
        return os.path.join('/static/weatherimages', 'thunderstorm.png')

if __name__ == '__main__':
    app.run(debug=True)
