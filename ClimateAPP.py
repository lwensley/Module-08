
# To run, go to folder, right click & select "Open Terminal at Folder"
# In terminal, type each of the following lines, hitting return after each line.
#   ls
#   conda env list
#   conda activate PythonData
#   python ClimateAPI.py


##########################################
# Imports
##########################################

import pandas as pd
import datetime as dt
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



##########################################
# Database Setup
##########################################

""" create engine """
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

""" reflect an existing database into a new model"""
Base = automap_base()

""" reflect the tables"""
Base.prepare(engine, reflect=True)

""" save references to each table"""
Measurement = Base.classes.measurement
Station = Base.classes.station

""" create a session (link) from Python to the DB"""
session = Session(engine)

automap_base().prepare(create_engine("sqlite:///Resources/hawaii.sqlite"), reflect=True)
    


##########################################
# Flask Setup
##########################################

app = Flask(__name__)


# Flask Routes

@app.route("/")

#Home page.
#List all routes that are available.

def welcome():
    return (
         f"Welcome to the Surfs Up API<br/><br/>"

         f"Data collected from 2010-01-01 to 2017-08-23 <br/><br/>"

         f"Available routes:<br/>"

         f"Last 12 months of available precipitation data:<br/>"
         f"/api/v1.0/prcp <br/><br/>"

         f"List of stations in the dataset:<br/>"
         f"/api/v1.0/station <br/><br/>"

         f"Last 12 months of available temperature observations:<br/>"
         f"/api/v1.0/tobs <br/><br/>"

         f"Average, Max, and Min temperature from any date to 2017-08-23:<br/>"
         f"/api/v1.0/yyyy-mm-dd <br/><br/>"

         f"Average, Max, and Min temperature between two dates:<br/>"
         f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd  <br/>"
     )


@app.route("/api/v1.0/prcp")

def prcp():

     """ Query the data for precipitation """
     prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()
    
     """ Convert the query results into a dictionary """
     prcp_results = [prcp_data]

     """ Return the JSON representation of the precipitation dictionary"""
     return jsonify(prcp_results)


@app.route("/api/v1.0/station")
def station():

     """ Query the data """
     station_data = session.query(Station.name).all()

     """ Create a list of stations from query results """
     station_list= list(np.ravel(station_data))

     """ Return the JSON representation of the precipitation dictionary"""
     return jsonify(station_list)



@app.route("/api/v1.0/tobs")
def tobs():
    
     """ Query the data """
     tobs_data = session.query(Station.name, Measurement.date, Measurement.tobs)\
                    .filter(Measurement.station == Station.station)\
                    .filter(Measurement.date > '2016-08-23')\
                    .order_by(Measurement.date).all()

     """ Create a dictionary from the row data and append to a list of results """
     tobs_results = []

     for row in tobs_data:
         tobs_dict = {}
         tobs_dict["station"] = row[0]
         tobs_dict["date"] = row[1]
         tobs_dict["tobs"] = row[2]
         tobs_results.append(tobs_dict)

     """Return a JSON list of Temperature Observations (tobs) for the last year of the data set"""
     return jsonify(tobs_results)


@app.route("/api/v1.0/<start>")
def calc_temps_data(start):

     

     """ Query the data """
     temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
           filter(Measurement.date >= start).all()

     """ Create a dictionary from the row data and append to a list of results """
     temp_results = []

     for row in temp_stats:
          temp_dict = {}
          temp_dict["start date"] = start
          temp_dict["end date"] = "2017-08-23"
          temp_dict["min temp"] = float(row[0])
          temp_dict["avg temp"] = float(row[1])
          temp_dict["max temp"] = float(row[2])
          temp_results.append(temp_dict)

     return jsonify(temp_results)


@app.route("/api/v1.0/<start>/<end>")
def calc_temp_period(start, end):

     """ Query the data """
     calc_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

     """ Create a dictionary from the row data and append to a list of results """
     calc_results = []

     for row in calc_stats:
          calc_dict = {}
          calc_dict["start date"] = start
          calc_dict["end date"] = end
          calc_dict["min temp"] = float(row[0])
          calc_dict["avg temp"] = float(row[1])
          calc_dict["max temp"] = float(row[2])
          calc_results.append(calc_dict)

     return jsonify(calc_results)

if __name__ == "__main__":
     app.run(debug=True)