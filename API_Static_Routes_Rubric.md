# Rubric and guide for the API_Static_Routes 

Use this guide to find where the required items for grading can be found within the app.py file 

API Static Routes (15 points)
---------------------------------------------------------------------------------

To receive all points, your Flask application must include:

1. A precipitation route that:

* Returns json with the date as the key and the value as the precipitation (3 points)

    Data in the form:
    [
      {
        "2016-08-23": 0.0
      },
      ...
    ]
    :return: json precipitation data

* Only returns the jsonified precipitation data for the last year in the database (3 points)

    last_12_months = session.query(Measurement.date,
                                   Measurement.prcp)\
                        .where(Measurement.date >= ONE_YEAR_PRIOR_DATE)\
                        .order_by(Measurement.date)\
                        .all()
    
    precipitation_dict = [{item.date: item.prcp} for item in last_12_months]
    return jsonify(precipitation_dict)

2. A stations route that:

* Returns jsonified data of all of the stations in the database (3 points)

  Data in the form:
    
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

3. A tobs route that:

* Returns jsonified data for the most active station (USC00519281) (3 points)
* Only returns the jsonified data for the last year of data (3 points)

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
                                   .where(Measurement.date >= ONE_YEAR_PRIOR_DATE,
                                          Measurement.station == MOST_ACTIVE_STATION)\
                                   .all()
    most_active_tobs_dict = [{item.date: item.tobs} for item in most_active_tobs_data]
    return jsonify(most_active_tobs_dict)


API Dynamic Route (15 points)
---------------------------------------------------------------------------------

To receive all points, your Flask application must include:

1. A start route that:

* Accepts the start date as a parameter from the URL (2 points)

def start(start: str):
    """Return temperature data from the `start` date to the end of the data set.

    :param start: string start date in YYYY-MM-DD form
    :return: json data
    """
    data = temperature_date_range_data(start, MOST_RECENT_DATE)
    return jsonify(data)

* Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset (4 points)

********************************* 

2. A start/end route that:

* Accepts the start and end dates as parameters from the URL (3 points)

def start_end_range(start: str, end: Union[str, dt.date]):

    """Return temperature data in the date range `start` to `end`.

    :param start: string start date in YYYY-MM-DD form
    :param end: string end date in YYYY-MM-DD form
    :return: json data
    """
    data = temperature_date_range_data(start, end)
    return jsonify(data)

* Returns the min, max, and average temperatures calculated from the given start date to the given end date (6 points)

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

