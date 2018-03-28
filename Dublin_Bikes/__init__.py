from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import app_config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+mysqlconnector://CGSdatabase:password@dublinbikes.ctaptplk7c5t.eu-west-1.rds.amazonaws.com/dublinbikes', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    import Dublin_Bikes.models
    Base.metadata.create_all(bind=engine)

    from Dublin_Bikes import models
    
    #makes app use the home blueprint
    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app