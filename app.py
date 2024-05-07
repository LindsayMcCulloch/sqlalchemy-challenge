# Import the dependencies.

import datetime as dt
from pathlib import Path
from typing import Dict, Union
from flask import Flask, jsonify
from sqlalchemy import create_engine, desc, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

#################################################
# Database Setup
#################################################

# Correctly generate the engine to the correct sqlite file (2 points)

db_path = Path(__file__).parent / "Resources/hawaii.sqlite"
engine = create_engine("sqlite:///" + str(db_path),
                       connect_args={'check_same_thread': False})

# Use automap_base() and reflect the database schema (2 points)

Base = automap_base()

# Correctly save references to the tables in the sqlite file (measurement and station) (2 points)

Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement`

Measurement = Base.classes["measurement"]

# the station class to a variable called `Station`

Station = Base.classes["station"]

# Correctly create and binds the session between the python app and database (2 points)

session = Session(bind=engine)

# Defining most active station for use in analysis file
def most_active_station() -> str:
    """Gives the most active station from the database

    Should be 'USC00519281'

    :return: string station
    """
    active_stations = session.query(Measurement.station,
                                    func.count(Measurement.station).label("count"))\
                             .join(Station, Measurement.station == Station.station)\
                             .group_by(Measurement.station)\
                             .order_by(desc("count"))\
                             .all()
    return active_stations[0].station 


most_recent_date = dt.datetime.strptime(session.query(func.max(Measurement.date)).scalar(), r"%Y-%m-%d").date()
one_year_data = most_recent_date - dt.timedelta(days=365)
most_active_station_constant = most_active_station()

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# Display the available routes on the landing page (2 points)

@app.route("/")
def home():
    """Landing page listing all the routes"""
    return"""
          <h1>Welcome to Module 10 Challenge</h1>
          <h2>Climate app of Hawaii data</h2>
          <h3>Available routes for this data:</h3>
          /api/v1.0/precipitation</br>
          /api/v1.0/stations</br>
          /api/v1.0/tobs</br>
          /api/v1.0/&lt;start&gt;</br>
          /api/v1.0/&lt;start&gt;/&lt;end&gt;</br>
          </br>
          &lt;start&gt; and &lt;end&gt; date format should be "YYYY-MM-DD"</br>
          Example: 2023-05-07
          """
@app.route("/api/v1.0/precipitation")
def precipitation():
    """
    Return the last 12 months of precipitation data for all stations.

    Data in the form:
    [
      {
        "2016-08-23": 0.0
      },
      ...
    ]
    :return: json precipitation data
    """
    last_12_months = session.query(Measurement.date,
                                   Measurement.prcp)\
                        .where(Measurement.date >= one_year_data)\
                        .order_by(Measurement.date)\
                        .all()
    
    precipitation_dict = [{item.date: item.prcp} for item in last_12_months]
    return jsonify(precipitation_dict)
@app.route("/api/v1.0/stations")
def stations():
    """Returns data with list of all stations
    Data in the form:
    {
      "stations":[
         "USC00519397",
         ...
      ]
    }
    :return: json data
    """
    stations = session.query(Station.station).all()
    stations_dict = {"stations": [value for (value,) in stations]}
    return jsonify(stations_dict)
@app.route("/api/v1.0/tobs")
def tobs():
    """Returns temperature data for the most active station in the last year of the data set.
    Data in the form:
    [
      {
        "2016-08-23": 77.0
      },
      ...
    ]
    :return: json data
    """
    most_active_tobs_data = session.query(Measurement.date,
                                          Measurement.tobs)\
                                   .where(Measurement.date >= one_year_data,
                                          Measurement.station == most_active_station_constant)\
                                   .all()
    most_active_tobs_dict = [{item.date: item.tobs} for item in most_active_tobs_data]
    return jsonify(most_active_tobs_dict)
@app.route("/api/v1.0/<start>")
def start(start: str):
    """Return temperature data from the `start` date to the end of the data set.

    :param start: string start date in YYYY-MM-DD form
    :return: json data
    """
    data = temperature_date_range_data(start, most_recent_date)
    return jsonify(data)
@app.route("/api/v1.0/<start>/<end>")
def temperature_date_range_all_data(start: str, end=None) -> Dict[str, float]:
    """Calculates the Min, Max, Average of temperatures from the `start` date to the end of the dataset.
    :param start: string start date in YYYY-MM-DD form
    :param end: string end date in YYYY-MM-DD form (default None)
    :return: dictionary containing temperature statistics
    """
    if end is None:
        end = session.query(func.max(Measurement.date)).scalar()
    
    temp_data = session.query(func.min(Measurement.tobs).label("TMIN"),
                               func.max(Measurement.tobs).label("TMAX"),
                               func.avg(Measurement.tobs).label("TAVG"))\
                         .filter(Measurement.date >= start,
                                 Measurement.date <= end)\
                         .one()
    
    data = {"TMIN": temp_data.TMIN, "TMAX": temp_data.TMAX, "TAVG": temp_data.TAVG}
    
    return data
def start_end_range(start: str, end: Union[str, dt.date]):
    """Return temperature data in the date range `start` to `end`.

    :param start: string start date in YYYY-MM-DD form
    :param end: string end date in YYYY-MM-DD form
    :return: json data
    """
    data = temperature_date_range_data(start, end)
    return jsonify(data)
def temperature_date_range_data(start: str, end: Union[str, dt.date]) -> Dict[str, float]:
    """Calculates the Min, Max, Average of temperatures in the  date range `start` to `end`.
    :param start: string start date in YYYY-MM-DD form
    :param end: string end date in YYYY-MM-DD form
    :return: list containing dictionary  
    """
    temp_data = session.query(func.min(Measurement.tobs).label("TMIN"),
                              func.max(Measurement.tobs).label("TMAX"),
                              func.avg(Measurement.tobs).label("TAVG"))\
                        .where(Measurement.date >= start,
                            Measurement.date <= end)\
                        .one()
    data = {"TMIN": temp_data.TMIN, "TMAX": temp_data.TMAX, "TAVG": temp_data.TAVG}
    return data
if __name__ == "__main__":
    app.run(debug=True)
    session.close()