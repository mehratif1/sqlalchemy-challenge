# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
import datetime as dt
from flask import Flask , jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
Measurement =Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB

session = Session(engine)
#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def homepage():
    """List of all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# Converting the query results from the precipitation analysis (last 12 months data) to a dictionary with date as key and prcp as vlaues
@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    print("Last Year Date:", last_year_date)

    last_year_data = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= last_year_date).all()

# Process the query results into a dictionary
    precipitation_dict = {date: prcp for date, prcp in last_year_data}

# Return the JSON representation using Flask's jsonify function
    return jsonify(precipitation_dict)


#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    # Query the database to retrieve the list of stations
    stations_data = session.query(Station.station).all()

    # Process the query results into a JSON list
    stations_list = [station[0] for station in stations_data]

    # Return the JSON response using Flask's jsonify function
    return jsonify(stations=stations_list)

#Query the dates and temperature observations of the most-active station for the previous year of data.

@app.route("/api/v1.0/tobs")   
def temperature():
    last_year_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    print("Last Year Date:", last_year_date)

    tobs_data = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281', Measurement.date >=last_year_date).all()
    tobs_data

 # Process the query results into a list
    tobs_list = [tobs[0] for tobs in tobs_data]

# Return the JSON response using Flask's jsonify function
    return jsonify(temperature_observations=tobs_list)

#For a specified start date, calculating TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
@app.route("/api/v1.0/<start>")
def temperature_start(start):
    # Convert the start date string to a datetime object
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')

    # Query TMIN, TAVG, and TMAX for dates greater than or equal to the start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start_date)\
        .all()

    # Create a JSON response
    temp_stats = [{
        "Start Date": start,
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }]

    return jsonify(temp_stats)


#For a specified start date and end date, calculating TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start, end):
    # Convert the start and end date strings to datetime objects
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')

    # Query TMIN, TAVG, and TMAX for dates within the specified range
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start_date, Measurement.date <= end_date)\
        .all()

    # Create a JSON response
    temp_stats = [{
        "Start Date": start,
        "End Date": end,
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }]

    return jsonify(temp_stats)

if __name__ == "__main__":
    app.run(debug=True)







    
