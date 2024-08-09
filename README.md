*Weather Data Database Insertion*
---
**Description**
---
- Makes calls to the Weatherstack API and processes the response before inserting it into a MongoDB Atlas collection
- Processes the data, adding helpful contextual information such as the fahrenheit symbol to the temperature
- Then passes the data through to MongoDB using pymongo

**Dependencies**
---
These libraries are required for the functionality of the program:
- Pymongo
- requests
- dnspython
- dotenv

**Running the program**
---
This program is simply run, and does not have an elaborate user interface

**Functionality**
---
- weatherData.py defines an array of cities, dates (in YYYY-MM-DD format), and timezones (ex. America/New_York)
- A connection to MongoDB is established by the usage of a connection string
- The function getWeatherStackData passes three arguments (city, date, timezone_id), and then formats the desired params and format of the API response after making the call
- To ensure that minimal database entries are created, the usage of nested structures is implemented: the location data is only passed through once per day per city, as opposed to once per city per hour (15 entries instead of 360)
- Data is printed to the console as it is entered into the database to provide some feedback for the user
- Errors are noted and passed to the user via the console
- A for loop handles the changing between different date/city combos to ensure that all 3 cities have complete reporting

**License**
---
This program is MIT licensed.




