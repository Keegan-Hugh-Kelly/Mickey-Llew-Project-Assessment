# Mickey-Llew-Project-Assessment
## Weather Forecast Web Application
##### Created by: Keegan.H Kelly
> The purpose of this assessment is to demonstrate my ability to extract data from a public API (OpenWeatherApp), process the data, and display the data in a meaningful visualization.
---
# Documentation
## Overview
`weather_visualization.py` is a Python script that serves as a web application to visualize weather data and forecast for various cities. It utilizes `Flask`for web development, `OpenWeatherMap` API to retrieve weather information, and SQLite database to store contact messages. The application allows users to view current weather, weather forecast, and weather data presented in tables, graphs, and maps.

## Requirements
To run this script, you need the following prerequisites:

- Python3
- Flask
- requests
- folium
- pandas
- flask_sqlalchemy
- jinja2`

You can install the required packages using `pip install -r requirements.txt`

## Configuration
Before running the script, ensure that you have the following configurations:

### OpenWeatherMap API Key: 
Obtain an **API key** from OpenWeatherMap and replace the `API_KEY` variable in the script with your key.

### API Key Name: 
If you have multiple API keys, change the `API_KEY_NAME` variable to a descriptive name for your key.

### Default City: 
The default city for weather data is set to *'Cape Town'*. You can change the `CITY` variable to your preferred city.

### Units: 
The units for temperature are set to *'metric'* **(Celsius)** by default. If you prefer **Fahrenheit**, change the `UNITS` variable to *'imperial'*.

### SQLite Database:
 The script uses a SQLite database to store contact messages. The database will be automatically created when the script is run. The database file will be named contact_messages.db, and it will be located in the same directory as the script.

### Running the Application:
To run the application, execute the script in the terminal:

> **bash**
> `python weather_visualization.py`

The application will run on a local server with debugging enabled (debug=True). You can access it by navigating to http://127.0.0.1:5000/ in your web browser.

**Routes and Endpoints**
---
- `/`: The home page displays the current weather data for the default city and a weather forecast for the next few days.

- `/search`: Allows users to search for weather data for different cities. After searching, users will be redirected to the appropriate page based on the referring URL (e.g., weather_map, weather_graphs, weather_tables, or index).

- `/weather-map`: Shows a map displaying the weather data for the current city.

- `/weather-graphs`: Displays graphs for weather data (temperature, precipitation, wind speed, humidity, etc.) for the next few days.

- `/weather-tables`: Displays weather forecast data in tabular format for the next few days.

- `/contact`: Provides a form for users to submit contact messages. The messages are stored in the SQLite database.

## Helper Functions
The script includes several helper functions:

- `get_weather_data`: Retrieves the current weather data from the OpenWeatherMap API for the specified city.

- `get_weather_forecast`: Retrieves the weather forecast data from the OpenWeatherMap API for the specified city. It also calculates aggregate values for each day (e.g., maximum temperature, minimum temperature, precipitation, etc.).

- `degrees_to_compass`: Converts wind direction in degrees to a human-readable compass direction (e.g., N, NE, E, etc.).

- `get_cloud_coverage_graphic`: Returns the URL of an image representing the weather condition based on the provided weather description.

## Templates
The script uses Jinja2 templating engine for rendering HTML templates. The templates are located in the templates folder and include the following:

- `index.html`: Template for the home page showing the current weather and weather forecast.

- `weather_map.html`: Template for displaying weather data on a map.

- `weather_graphs.html`: Template for displaying weather data in graphs.

- `weather_tables.html`: Template for displaying weather forecast data in tabular format.

- `contact.html`: Template for the contact form.

- `error.html`: Template for displaying error messages.

## Database Model
The script defines a database model ContactMessage using Flask SQLAlchemy to store contact messages. The model has the following fields:

- `id`: Integer field (primary key).
- `email`: String field (max length: 120 characters, not nullable).
- `message`: Text field (not nullable).
# Design
The CSS styling for the web application was designed to match the company's color palette and theme. A vibrant shade of yellow (#FFD100) is consistently used for buttons and background highlights, reflecting the weather and climate theme. The clean white background (#FFFFFF) complements the yellow accents, enhancing readability and providing a modern look. The "Chillax" font-family adds a playful and relaxed vibe, aligning with the company's identity. Overall, the styling creates a visually cohesive and engaging user experience in line with the weather and relaxation theme.
## File Structure and Organization:
The application is built using `Flask`, a popular Python web framework.
The `weather_visualization.py` file contains the main application code, including routes and database setup.
The `templates` folder contains HTML templates for rendering the web pages.
The `static` folder contains static assets like CSS stylesheets, images, and JavaScript files.
## Dependencies:
The app uses various external libraries and APIs to handle different tasks:
- `Flask`: For web application development.
- `Requests`: For making API requests to the OpenWeatherMap API.
- `Folium`: For displaying maps.
- `Jinja2`: For template rendering.
- `pandas`: For data manipulation.
- `Flask-SQLAlchemy`: For managing the SQLite database.
## Flask App and Database Setup:
- The `Flask` app is created and configured with an `SQLite` database.
- The `ContactMessage` model is defined to store contact form submissions in the database.
- The weather_visualization context is used to create the database and tables.
## Routes and URL Endpoints:
The `main route (/)` renders the index.html template, displaying the weather data and forecast for the default city.
The `search route (/search)` handles city search and redirects to different weather views based on the referrer.
The `weather_map route (/weather-map)` renders the weather_map.html template, displaying a map with the weather data.
The `weather_graphs route (/weather-graphs)` renders the weather_graphs.html template, displaying weather graphs.
The `weather_tables route (/weather-tables)` renders the weather_tables.html template, displaying weather data in tabular format.
The `contact route (/contact)` handles the contact form submission.
## Weather Data and Forecast:
The `get_weather_data` function retrieves the current weather data for the specified city using the OpenWeatherMap API.
The `get_weather_forecast` function retrieves the weather forecast data for the specified city using the OpenWeatherMap API.
The functions handle API responses and extract relevant weather information.
## Jinja2 Templating:
The templates are written in `Jinja2`, a template engine for Python.
The templates use Jinja2 tags and filters to insert dynamic data into the HTML pages.
The include statement is used to reuse the `navbar` and `footer` across multiple templates.
The `tojson` filter is used to convert Python data to JSON for passing it to JavaScript code.
## Frontend Styling:
The app uses the `Bootstrap CSS framework` to style the pages.
The weather cards in index.html use `CSS classes` to style weather data and display weather images.
The footer contains social media icons with links to external pages.
## JavaScript and Leaflet:
The Leaflet JavaScript library is used to display the weather map on `weather_map.html`.
The JavaScript code initializes the map, adds a tile layer, and places a marker on the map with weather data as a popup.
## Form Handling and Database Interaction:
The contact.html template renders a contact form.
The contact route handles POST requests, saving the contact form data (email and message) in the database using SQLAlchemy.
## Error Handling:
The app handles exceptions and displays error messages in case of API call failures or other exceptions.
# Insights
Through this project assessment, I gained valuable experience in working with web development, API integration, data extraction, and data visualization using Python and Flask. I successfully implemented the OpenWeatherMap API to retrieve weather data for various cities, processed the data to present it in meaningful visualizations, and allowed users to interact with the application through different routes and endpoints.

The use of Flask, along with Jinja2 templating engine, made it easier to create dynamic web pages and render data seamlessly. The integration of external libraries such as Folium, pandas, and SQLAlchemy enhanced the functionality of the application and enabled me to store contact messages in an SQLite database.

Overall, this project assessment demonstrated my ability to handle real-world data, interact with APIs, and present information in a user-friendly and visually appealing manner. I feel confident in my skills as a Python developer and have a better understanding of building web applications for data visualization purposes. I am eager to apply these skills in future projects and continue exploring new technologies to further enhance my abilities.
# Conclusion
The `weather_visualization.py` script is a web application that utilizes Flask and various libraries to extract and visualize weather data from the `OpenWeatherMap` API. Users can view current weather data and forecasts for different cities presented in tables, graphs, and maps. The application showcases my API handling and Data Visualization skills effectively.