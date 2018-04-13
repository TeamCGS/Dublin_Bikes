import json
import requests
from sqlalchemy import Column, Integer, String, Float, Boolean
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from base_file import Base
import time
import datetime

class Weather(Base):
    """
    Create a Weather table
    """
    __tablename__ = 'weather1'
    
    id = Column(Integer, nullable=False, primary_key ='True')
    name = Column(String(100), nullable = False)
    humidity = Column(Integer ,nullable = False)
    temp = Column(Integer, nullable=False)
    temp_max = Column(Integer, nullable=False)
    temp_min = Column(Integer, nullable=False)
    description = Column(String(100), nullable = False)
    icon = Column(String(100), nullable = False)
    main_description = Column(String(100), nullable = False)
    timeDate = Column(String (100), primary_key=True, nullable=False)
    
    
    def getWeatherData(self):
       
        weather_engine = create_engine('mysql+mysqlconnector://CGSdatabase:password@dublinbikes.ctaptplk7c5t.eu-west-1.rds.amazonaws.com/dublinbikes', convert_unicode=True) 
        Session = sessionmaker(bind=weather_engine)
        talk_session = Session()
        Base.metadata.create_all(bind=weather_engine)
        
        while True:
            try:
        
                STATIONS_URI = "api.openweathermap.org/data/2.5/weather?"
                api_url = 'http://api.openweathermap.org/data/2.5/weather'
                appid = "033bc70c21f56a4af381b76c18f81458"  
                r = requests.get(url=api_url, params=dict(q='Dublin', APPID=appid))
                #pprint(r)
            
                data = r.json()
                #pprint(data)
                self.writeToDatabase(weather_engine,talk_session,data)
                time.sleep(30*60)
                
            except:
                if weather_engine is None:
                    print(traceback.format_exc())
        
        talk_session.close()
        return
        
    def writeToDatabase(self, weather_engine, talk_session, data):

        self.data = data 
        now = datetime.datetime.now()
    
        weather = Weather(id=self.data["id"],
                                    name=self.data["name"],
                                    humidity=self.data["main"]["humidity"],
                                    temp_max=self.data["main"]["temp_max"],
                                    temp_min=self.data["main"]["temp_min"],
                                    temp=self.data["main"]["temp"],
                                    description=self.data["weather"][0]["description"],
                                    icon=self.data["weather"][0]["icon"],
                                    main_description=self.data["weather"][0]["main"],
                                    timeDate=now)
    
        talk_session.add(weather)
        talk_session.commit()
        
        return


