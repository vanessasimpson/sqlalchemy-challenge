import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)



#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation_data = session.query(func.strftime("%Y-%m-%d", Measurement.date), Measurement.prcp).filter(func.strftime("%Y-%m-%d", Measurement.date) >= dt.date(2016, 8, 23)).all()
    precipitation_data
    precip = {date:prcp for date, prcp in precipitation_data}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    all_stations = session.query(Station.Station).all()
    stations = list(np.ravel(all_stations))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def tobs():
    observation_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281").filter(func.strftime("%Y-%m-%d", Measurement.date) >= '2016-08-23').all()
    observations = list(np.ravel(observation_data))
    return jsonify(observations=observations)

def date_stats(start):
    sel = [ 
       func.min(Meaurement.tobs), 
       func.max(Meaurement.tobs), 
       func.avg(Meaurement.tobs)] 
    data = session.query(*sel).filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).all()
    results = list(np.ravel(data))
    return jsonify(results)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def date_stats(start,end=None):
    if end is None:
        sel = [ 
        func.min(Meaurement.tobs), 
        func.max(Meaurement.tobs), 
        func.avg(Meaurement.tobs)] 
        data = session.query(*sel).filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).all()
        results = list(np.ravel(data))
    return jsonify(results)
    else:    
        sel = [ 
        func.min(Meaurement.tobs), 
        func.maxd(Meaurement.tobs), 
        func.avg(Meaurement.tobs)] 
        data_2 = session.query(*sel).filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).filter(func.strftime("%Y-%m-%d", Measurement.date) <= end).all()
        results_2 = list(np.ravel(data_2))
        return jsonify(results_2)


"""TODO: Handle API route with variable path to allow getting info
for a specific character based on their 'superhero' name """


if __name__ == "__main__":
    app.run(debug=True)

