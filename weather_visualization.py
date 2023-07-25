import requests
import matplotlib.pyplot as plt

API_KEY = 'c15281beae1e4915fef587ae1b1382ce'  # Change to your API key
API_KEY_NAME = 'default' # Change to your API key name
CITY = 'Cape Town'  # Change to your city
UNITS = 'metric'  # Change to 'imperial' for Fahrenheit

def get_weather_data():
    url = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&units={UNITS}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    if 'main' not in data:
        raise Exception(f"Error: Unable to retrieve weather data. Response: {data}")
        
    return data

def plot_weather_data(weather_data):
    temperature = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']

    plt.bar(['Temperature', 'Humidity'], [temperature, humidity])
    plt.ylabel('Value')
    plt.title(f'Weather in {CITY}')
    plt.show()

if __name__ == '__main__':
    try:
        weather_data = get_weather_data()
        plot_weather_data(weather_data)
    except Exception as e:
        print(e)
