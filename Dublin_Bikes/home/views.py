from flask import Flask, render_template, jsonify, g
from . import home
from sqlalchemy import create_engine

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
    sql = "select * from Static_Data;"
    rows = conn.execute(sql).fetchall()
    stations = []
    for row in rows:
        stations.append(dict(row))
    return jsonify(stations=stations) 