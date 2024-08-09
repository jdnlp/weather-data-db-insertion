# begin by importing the requests library - have to have installed it via (pip install requests) first
# import pymongo in order to be able to store data in MongoDB
# import dns.resolver to set the nameserver to Google's public DNS server - this was to fix a DNS issue that I kept running into - but may not be necessary
# import dotenv to access the API key stored in the .env file
# import os to access the environment variable
import requests
from pymongo import MongoClient
import dns.resolver
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']
from dotenv import load_dotenv
import os

# Load keys from .env file - you have to enter your keys in the keys.env file, and it has to be in the same directory as this file for this path to work
load_dotenv('keys.env')

# Access the keys stored in the .env file
mongoDB_connection_string = os.getenv("MONGODB_CONNECTION_STRING")
apiKey = os.getenv("API_KEY")


# Define cities and corresponding time zones
cities = ["Atlanta", "New York", "San Francisco"]
dates = ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"]
timezones = ["America/New_York", "America/New_York", "America/Los_Angeles"]

# Connect to MongoDB
client = MongoClient(mongoDB_connection_string)
db = client['weatherData']
collection = db["unitedStatesWeather"]

# Function to retrieve weather data
def getWeatherStackData(city, date, timezone_id):
    api_url = "http://api.weatherstack.com/historical"

    daily_data = {
        'location': None,  # To be filled with location data
        'weather': {
            date: {}  # To store hourly data for the date
        }
    }
    
    for i in range(0, 2400, 100):  # Loop through hours in increments of 100 (e.g., 0000, 0100, 0200, ... 2300)
        hour_str = str(i).zfill(4)  # Converts i to a 4-digit string (e.g., 0 -> "0000", 100 -> "0100", ...)
        hour_str = hour_str[:2] + ":" + hour_str[2:]  # Inserts a colon to separate hours and minutes
        params = { # Parameters that are sent to the Weatherstack API to specify the needed information
            'access_key': apiKey,
            'query': city,
            'historical_date': date,
            'timezone_id': timezone_id,
            'hourly': 1,
            'interval': 1,
            'units': 'f', # Temperature in Fahrenheit
        }

        response = requests.get(api_url, params=params)
        data = response.json()
        
        if 'error' in data: # error reporting
            print(f"Error retrieving data for {city} on {date} at hour {i}: {data['error']}")
            continue
        
        if 'location' not in data or 'historical' not in data:
            print(f"Error: 'location' or 'historical' key not found in API response for {city} on {date} at hour {i}.")
            print(f"API response: {data}")
            continue

        # Extracting data for the current hour
        hourly_data = data['historical'][date]['hourly'][i//100]  # Convert i to index by dividing by 100
        
        if daily_data['location'] is None:
            # Only setting location data once to keep entries into db minimal
            daily_data['location'] = {
                'name': data['location']['name'],
                'country': data['location']['country'],
                'region': data['location']['region']
            }
        
        # Adding the hourly data to the daily_data structure
        daily_data['weather'][date][hour_str] = {
            'temperature': f"{hourly_data['temperature']}°F",
            'weather_descriptions': hourly_data['weather_descriptions'],
            'humidity': f"{hourly_data['humidity']}%"
        }
    
    # Print and store the accumulated data for the entire day
    print(daily_data)
    collection.insert_one(daily_data)

# Iterate over cities and dates
for city, timezone_id in zip(cities, timezones):
    for date in dates:
        getWeatherStackData(city, date, timezone_id)