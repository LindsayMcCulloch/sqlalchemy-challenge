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

#Defining most active station
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
    return active_stations[0].station  # selecting from named tuple


MOST_RECENT_DATE = dt.datetime.strptime(session.query(func.max(Measurement.date)).scalar(), r"%Y-%m-%d").date()
ONE_YEAR_PRIOR_DATE = MOST_RECENT_DATE - dt.timedelta(days=365)
MOST_ACTIVE_STATION = most_active_station()

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################
