# Mickey-Llew-Project-Assessment
### By: Keegan.H Kelly
### The purpose of this assessment is to demonstrate my ability to extract data from a public API (OpenWeatherApp), process the data, and display the data in a meaningful visualization.
---
# Setting Up The Dev Environment:

1. I began the project but initalizing a repo to keep track of changes made to the code and to allow access to others you would like to use the script. (`GitHub Desktop`)

2. I decided to use `Python` as my choice of language due to how versatile and the extensive collection of libraries to choose from to best represent the data.

3. In the console, I ran this command to install the library `matplotlib` for data visualization.

The command: `pip install requests matplotlib`

4. Since we are using Open Weather as our API of choice, I signed up and got an API key to authenticate the requests I make to the API.

API_Key: `c15281beae1e4915fef587ae1b1382ce`

API_Name: `Default`

5. Next we begin writing the Python Script itself, the file is called `weather_visualization.py`.


# Documentation:
## 1. How the script functions
---

### Imported Libraries:
We begin by importing the two libraries we will need:

The request module allows you to send HTTP requests using Python and our API. The matplotlib allows you to create a plotting area in a figure, plots some lines in a plotting area, decorates the plot with labels. This is the visualization aspect of the project.

line1:`import requests`

line2:`import matplotlib.pyplot as plt`

### API Key / Settings:

The next section of code is responsible with authentication by using our `API_KEY` to communicate with the Open Weater API. The `CITY` is to specify which city we want to pull our data for to be visualized. The `UNITS` is the format of how the data must be displayed either `Metric` for Celsius or `Imperial` for Fahrenheit.

line4: `API_KEY = 'c15281beae1e4915fef587ae1b1382ce'`

line5: `API_KEY_NAME = 'default'` 

line6: `CITY = 'Cape Town'`

line7: `UNITS = 'metric'`

### Functions:

The `get_weather_data` function is responsible for collecting and fetching the data from the OpenWeatherMap API using the `City`, `UNITS` and `API_KEY` to specify the city we want, the type of units (imperial or metric) and our API_Key to authenticate our script requesting the data.

The `display_temperature_on_map` function makes use of the latitude and longitude values to plot the temperature as tiles across the map for accurate temperature readings. `map_city` creates the map using the `folium` library. Next is the **Temperature Overlay** which pulls the temperature data from the OpenWeatherMap API which is then displayed as tiles across the map.

The `tooltip` displays the temperature in the correct unit by the mouse cursor when you hover over it on the map. 

The `map_city.save` function saves this in a embedded HTML file and prints the message in the terminal to help guide the user to run the HTML file on their browser.
## 2. Design
---



## 3. How to execute and run the data visualization
---
Create a terminal window inside VSC (Visual Studio Code IDE) that is inside the correct folder directory where the script is found. Use this command to run the script that will visualize the data of the city you specified:

`python3 weather_visualization.py`

You'll see a window appear displaying the data visualizer.

## 4. My insights obtained from the data visualization based off the data set
---