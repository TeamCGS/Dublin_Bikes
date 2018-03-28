from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import app_config
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    
    migrate = Migrate(app, db)
    from Dublin_Bikes import models
    
    #makes app use the home blueprint
    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)
    
    # temporary route
    #@app.route('/')
    #def hello_world():
    #   return 'Hello, World!'

    return app