from flask import Flask, render_template, jsonify, g
from . import home
from sqlalchemy import create_engine
import pandas as pd
import json
from pandas.core.datetools import day
from flask import request
import pickle
import os
from sklearn.externals import joblib
from _pydecimal import Rounded

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
          

# changed stations to get up to date data aswell so the markers can be populated with different colors
@home.route('/stations') 
def get_stations(): 
    conn = get_db()
    sql = "SELECT * from Static_Data JOIN Stations Where Static_Data.number = Stations.number;"
    rows = conn.execute(sql).fetchall()
    stations = []
    for row in rows:
        stations.append(dict(row))
    return jsonify(stations=stations)


@home.route('/forcast') 
def get_forcast(): 
    conn = get_db()
    sql = "SELECT DISTINCT day, day_num FROM weather_prediction;"
    rows = conn.execute(sql).fetchall()
    days = []
    for row in rows:
        days.append(dict(row))
    return jsonify(days=days)




@home.route('/station_availability/<station_number>') 
def get_dynamic_data(station_number):
    conn = get_db()
    sql = "select * from Stations where number="+station_number+";"
    rows = conn.execute(sql).fetchall()
    stations = []
    for row in rows:
        stations.append(dict(row))
    return jsonify(stations=stations)

@home.route('/occupancyOfAvailableBikeStandsDaily/<station_number>') 
def get_AvailableBikeStandsOccupancy_dataDaily(station_number):
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

@home.route('/occupancyOfAvailableBikeStandsHourly/<station_number>') 
def get_AvailableBikeStandsOccupancy_dataHourly(station_number):
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
    res = df['available_bike_stands'].resample('1h').mean()
    
#     print(res)
    return jsonify(data=json.dumps(list(zip(map(lambda x:x.isoformat(), res.index), res.values))))

@home.route('/occupancyOfAvailableBikesDaily/<station_number>') 
def get_AvailableBikesOccupancy_dataDaily(station_number):
    conn = get_db()
    params = {"number": station_number}
    sql_1 = '''
       select timeDate, available_bikes
       from JoinedTable
       where number = {number}
       order by timeDate
   '''.format(**params)
    #print("ooc", sql_1)
    df = pd.read_sql_query(sql_1, conn)
    #print("++++++++", df)
    df['last_update_date'] = pd.to_datetime(df.timeDate, format='%Y-%m-%d %H:%M:%S.%f')
    df.set_index('last_update_date', inplace=True)
    res = df['available_bikes'].resample('1d').mean()
    
    return jsonify(data=json.dumps(list(zip(map(lambda x:x.isoformat(), res.index), res.values))))

@home.route('/occupancyOfAvailableBikesHourly/<station_number>') 
def get_AvailableBikesOccupancy_dataHourly(station_number):
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
    res = df['available_bikes'].resample('1h').mean()
    
    return jsonify(data=json.dumps(list(zip(map(lambda x:x.isoformat(), res.index), res.values))))


@home.route('/modelPredictions', methods=['POST']) 
def modelPredictions():

    if request.method == 'POST':

        predictionStation = int(request.form['predictionStation'])
        day = int(request.form['days']) #string for the day of the week eg. monday
        time = int(request.form['time']) #24 hours eg.13 for one o'clock

       #this is needed as weather is only collected in hours of 3 
        if 0 < time < 4:
            time = 3
        elif 3 < time < 7:
            time = 6
        elif 6 < time < 10:
            time = 9
        elif 9 < time < 13:
            time = 12
        elif 12 < time < 16:
            time = 15
        elif 15 < time < 19:
            time = 18
        elif 18 < time < 22:
            time = 21
        else:
            time = 0
            
        params = {"day": day,
                  "time":time} 
        conn = get_db()
    
        sql = '''
                SELECT temp, rain 
                FROM dublinbikes.weather_prediction
                WHERE day_num = {day} AND hour = {time};
            '''.format(**params)
              
        df = pd.read_sql_query(sql, conn)
        df.insert(0,'station_number', predictionStation)
        df.insert(1,'day', day)
        df.insert(2,'time', time)
                        
        model = joblib.load('../Dublin_Bikes/Dublin_Bikes/home/model.p') #loading in the model from the file system

        prediction = model.predict(df)
        rounded_prediction = int(round(prediction[0]))        
        return jsonify(rounded_prediction) #reuturned to Ajax function

      

@home.route('/weather') 
def get_weather():
    conn = get_db()
    sql = "SELECT * FROM (SELECT * FROM weather1 ORDER BY timeDate DESC LIMIT 1 ) T1 ORDER BY timeDate"
    rows = conn.execute(sql).fetchall()
    weather = []
    for row in rows:
        #print(row)
        weather.append(dict(row))
    return jsonify(weather=weather)