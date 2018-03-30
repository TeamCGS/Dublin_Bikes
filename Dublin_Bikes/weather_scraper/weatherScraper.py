import json
import requests
from sqlalchemy import Column, Integer, String, Float, Boolean
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from base_file import Base

class Weather(Base):
    """
    Create a Weather table
    """
    __tablename__ = 'weather'
    
    id = Column(Integer, nullable=False, primary_key ='True')
    name = Column(String(100), nullable = False)
    temp = Column(Integer, nullable=False)
    temp_max = Column(Integer, nullable=False)
    temp_min = Column(Integer, nullable=False)
    #description = Column(String(100), nullable = False)
    
    
    def getWeatherData(self):
       
        weather_engine = create_engine('mysql+mysqlconnector://CGSdatabase:password@dublinbikes.ctaptplk7c5t.eu-west-1.rds.amazonaws.com/dublinbikes', convert_unicode=True) 
        Session = sessionmaker(bind=weather_engine)
        talk_session = Session()
    
        Base.metadata.create_all(bind=weather_engine)
        
        STATIONS_URI = "api.openweathermap.org/data/2.5/weather?"
        api_url = 'http://api.openweathermap.org/data/2.5/weather'
        appid = "033bc70c21f56a4af381b76c18f81458"  
        r = requests.get(url=api_url, params=dict(q='Dublin', APPID=appid))
        pprint(r)
    
        data = r.json()
        pprint(data)
        
        
        weather = Weather(id=data["id"],
                                    name=data["name"],
                                    temp_max=data["main"]["temp_max"],
                                    temp_min=data["main"]["temp_min"],
                                    temp=data["main"]["temp"])
                                    #descrption=data["weather"][0]["description"])
        talk_session.add(weather)
        talk_session.commit()  
        talk_session.close()
        


