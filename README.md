# sqlalchemy-challenge
This is the repository for Monash University Data Analytics Bootcamp Module 10 Challenge

# How to use
- Resources directory contains data source files:
* hawaii.sqlite
* hawaii_measurements.csv
* hawaii_stations.csv

- app.py contains the API SQLite Connection & Landing Page & Route queries
  
- API_Static_Routes_Rubric an be used to find where the code for grading is within the app.py file FLASK API code
  
-  Module_10_challange.ipynb is the main notebook for code and analysis

Background:
--------------------------------------------------------------------------------------------------------------------------------
Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area. The following sections outline the steps that you need to take to accomplish this task.

Part 1: Analyse and Explore the Climate Data
--------------------------------------------------------------------------------------------------------------------------------

In this section, you’ll use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. Specifically, you’ll use SQLAlchemy ORM queries, Pandas, and Matplotlib. To do so, complete the following steps:

1. Note that you’ll use the provided files (climate_starter.ipynb and hawaii.sqlite) to complete your climate analysis and data exploration.

2. Use the SQLAlchemy create_engine() function to connect to your SQLite database.

3. Use the SQLAlchemy automap_base() function to reflect your tables into classes, and then save references to the classes named station and measurement.

4. Link Python to the database by creating a SQLAlchemy session.

5. Perform a precipitation analysis and then a station analysis by completing the steps in the following two subsections.

Precipitation Analysis
--------------------------------------------------------------------------------------------------------------------------------

1. Find the most recent date in the dataset.

2. Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.

3. Select only the "date" and "prcp" values.

4. Load the query results into a Pandas DataFrame. Explicitly set the column names.

5. Sort the DataFrame values by "date".

6. Plot the results by using the DataFrame plot method

7. Use Pandas to print the summary statistics for the precipitation data.

Station Analysis
--------------------------------------------------------------------------------------------------------------------------------

1. Design a query to calculate the total number of stations in the dataset.

2. Design a query to find the most-active stations (that is, the stations that have the most rows). To do so, complete the following steps:

* List the stations and observation counts in descending order.

* Answer the following question: which station id has the greatest number of observations?

* Using the most-active station id, calculate the lowest, highest, and average temperatures.

3. Design a query to get the previous 12 months of temperature observation (TOBS) data. To do so, complete the following steps:

* Filter by the station that has the greatest number of observations.

* Query the previous 12 months of TOBS data for that station.

* Plot the results as a histogram with bins=12, 

4. Close your session.

Part 2: Design Your Climate App
--------------------------------------------------------------------------------------------------------------------------------

Now that you’ve completed your initial analysis, you’ll design a Flask API based on the queries that you just developed. To do so, use Flask to create your routes as follows

1. /

* Start at the homepage.

* List all the available routes.

2. /api/v1.0/precipitation

* Convert the query results to a dictionary by using date as the key and prcp as the value.

* Return the JSON representation of your dictionary.

3. /api/v1.0/stations

* Return a JSON list of stations from the dataset.

4. /api/v1.0/tobs

* Query the dates and temperature observations of the most-active station for the previous year of data.

* Return a JSON list of temperature observations for the previous year.

5. /api/v1.0/<start> and /api/v1.0/<start>/<end>

* Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

* For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

* For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

Resources used:
--------------------------------------------------------------------------------------------------------------------------------
BCS Xpert Learning assistant 

Office Hours

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

https://stackoverflow.com/questions/46401131/simple-flask-application-not-working

https://stackoverflow.com/questions/62776240/why-isnt-my-histogram-showing-on-jupyter-notebook#:~:text=1%20Answer&text=In%20the%20code%2C%20you%20are,gcf()%20or%20plt.

https://mode.com/example-gallery/python_histogram

https://stackoverflow.com/questions/23772165/flask-app-not-running-in-localhost?rq=3

https://stackoverflow.com/questions/52965956/flask-request-is-returning-404-not-found?rq=3

https://www.sitepoint.com/flask-url-routing/#:~:text=Flask%20allows%20you%20to%20create,string%20to%20your%20view%20function.

https://www.geeksforgeeks.org/flask-app-routing/

https://stackoverflow.com/questions/58177074/data-not-getting-comitted-to-database-in-flask-application
