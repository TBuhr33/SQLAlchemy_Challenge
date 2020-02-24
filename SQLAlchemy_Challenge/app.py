import numpy as np 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt 

#setup the database and ROM, same as jupyter notebook
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)

#create references
Station = Base.classes.station
Measurement = Base.classes.measurement 

#Setup FLASK

app = Flask(__name__)
@app.route('/')
def home():
    return(
        f"Hawaii Weather API.<br/><br/>"
        f"SEE AVAILABLE ROUTES BELOW:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/%start%<br/>"
        f"/api/v1.0/%start%/%end%<br/>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23')\
        .filter(Measurement.date <= '2017-08-23').all()
    session.close()

    prcp_data = []

    for date, prcp in data:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        prcp_data.append(prcp_dict)
        

    return jsonify(prcp_data)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    st_list = session.query(Station.station).all()
    session.close()

    stations = []

    for station in st_list:
        stations.append(station)

    return jsonify(stations)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    tobs_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23')\
        .filter(Measurement.date <= '2017-08-23').all()
    session.close()

    obs = []

    for date, tobs in tobs_data:
        data = {}
        data['date'] = date
        data['tobs'] = tobs
        obs.append(data)

    return jsonify(obs)

@app.route('/api/v1.0/%start%')
def st_date(strt_date):
    session = Session(engine)
    strt_date = '2015-03-31'
    tobs_st = session.query(Measurement.date, func.min(Measurement.tobs), \
        func.max(Measurement.tobs), func.avg(Measurement.tobs).filter(Measurement.date >= strt_date).group_by(Measurement.date).all())
    session.close()

    starts = []

    for date, max_start, avg_start in tobs_st:
        data_tobs = {}
        data_tobs['date'] = date
        data_tobs['min'] = min_start
        data_tobs['max'] = max_start
        data_tobs['avg'] = avg_start
        starts.append(data_tobs)
    
    return jsonify(starts)

@app.route('/api/v1.0/%start%/%end%')
def st_end(st_date, end_date):
    session = Session(engine)
    st_date = '2015-03-31'
    end_date = '2015-04-05'
    st_end_data =  session.query(Measurement.date, func.min(Measurement.tobs), \
        func.max(Measurement.tobs), func.avg(Measurement.tobs).filter(Measurement.date >= st_date)\
        .filter(Measurement.date <= end_date).group_by(Measurement.date).all())
    session.close()

    st_end_out = []

    for date, min_date, max_date, avg_date in st_end_data:
        temp = {}
        temp['date'] = date
        temp['min'] = min_date
        temp['max'] = max_date
        temp['avg'] = avg_date
        st_end_out.append(temp)

    return jsonify(st_end_out)

if __name__ =='__main__':
    app.run(debug = True)
    