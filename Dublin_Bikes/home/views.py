from flask import Flask, render_template, jsonify, g
from . import home
from sqlalchemy import create_engine
import pandas as pd
import json

def connect_to_database():
        engine = create_engine('mysql+mysqlconnector://CGSdatabase:password@dublinbikes.ctaptplk7c5t.eu-west-1.rds.amazonaws.com/dublinbikes', convert_unicode=True)
        return engine
      
def get_db():
    db = getattr(g, '_database', None)  
    if db is None:
        db = g._database = connect_to_database()
    return db

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    
    return render_template('home/index.html', title="Welcome") 
          
@home.route('/stations') 
def get_stations(): 
    conn = get_db()
    sql = "select * from Static_Data1;"
    rows = conn.execute(sql).fetchall()
    stations = []
    for row in rows:
        stations.append(dict(row))
    return jsonify(stations=stations)

@home.route('/station_availability/<station_number>') 
def get_dynamic_data(station_number):
    conn = get_db()
    sql = "select * from Stations1 where number="+station_number+";"
    rows = conn.execute(sql).fetchall()
    stations = []
    for row in rows:
        stations.append(dict(row))
    return jsonify(stations=stations)

@home.route('/occupancyOfAvailableBikeStands/<station_number>') 
def get_AvailableBikeStandsOccupancy_data(station_number):
    conn = get_db()
    params = {"number": station_number}
    sql = '''
       select timeDate, available_bike_stands
       from JoinedTable
       where number = {number}
       order by timeDate
   '''.format(**params)
    df = pd.read_sql_query(sql, conn)
    df['last_update_date'] = pd.to_datetime(df.timeDate, format='%Y-%m-%d %H:%M:%S.%f')
    df.set_index('last_update_date', inplace=True)
    res = df['available_bike_stands'].resample('1d').mean()
    
#     print(res)
    return jsonify(data=json.dumps(list(zip(map(lambda x:x.isoformat(), res.index), res.values))))

@home.route('/occupancyOfAvailableBikesByHour/<station_number>') 
def get_AvailableBikesOccupancy_data(station_number):
    conn = get_db()
    params = {"number": station_number}
    sql = '''
       select timeDate, available_bikes
       from JoinedTable
       where number = {number}
       order by timeDate
   '''.format(**params)
    df = pd.read_sql_query(sql, conn)
    df['last_update_date'] = pd.to_datetime(df.timeDate, format='%Y-%m-%d %H:%M:%S.%f')
    df.set_index('last_update_date', inplace=True)
    res = df['available_bikes'].resample('1d').mean()
    
    return jsonify(data=json.dumps(list(zip(map(lambda x:x.isoformat(), res.index), res.values))))