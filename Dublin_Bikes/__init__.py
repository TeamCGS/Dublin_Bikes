from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from config import app_config


def create_app(config_name):
    ''' This function makes the Dublin_Bikes app'''
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    
#     
#     @app.teardown_appcontext
#     def close_connection(exception):                DONT KNOW WHERE TO PUT
#         db = getattr(g, '_database', None)          THIS BLOCK OF CODE
#         if db is not None:                          APP CRASHES WHE I USE IT.
#             db.close()

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)
    
    return app