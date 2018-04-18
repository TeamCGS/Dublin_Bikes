import json
import requests

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import datetime
import time 
from weather_predictor_base import weather_base
import csv
from calendar import weekday


class Weather(weather_base):
    """
    Create a Weather table
    """
    __tablename__ = 'weather_prediction'
    
    humidity = Column(Integer ,nullable = False)
    temp = Column(Integer, nullable=False)
    temp_max = Column(Integer, nullable=False)
    temp_min = Column(Integer, nullable=False)
    description = Column(String(100), nullable = False)
    icon = Column(String(100), nullable = False)
    main_description = Column(String(100), nullable = False)
    day = Column(String(100),nullable =False)
    weekday = Column(String(100),nullable = False)
    weekend = Column(String(100),nullable = False)
    hour = Column(String(100),nullable=False)
    day_num =Column(String(100),nullable = False)
    rain = Column(Integer,nullable = False)
    timeDate = Column(String (100), primary_key=True, nullable=False)
    
    
    def getWeatherData(self):
       
        weather_engine_pred = create_engine('mysql+mysqlconnector://CGSdatabase:password@dublinbikes.ctaptplk7c5t.eu-west-1.rds.amazonaws.com/dublinbikes', convert_unicode=True) 
        Session = sessionmaker(bind=weather_engine_pred)
        talk_session = Session()
        weather_base.metadata.create_all(bind=weather_engine_pred)
        
        while True:
            try:
        
                api_url = 'http://api.openweathermap.org/data/2.5/forecast'
                appid = "033bc70c21f56a4af381b76c18f81458"  
                r = requests.get(url=api_url, params=dict(q='Dublin', APPID=appid))
                
                data = r.json()
                #pprint(data)
                
                self.writeToDatabase(weather_engine_pred,talk_session,data)
                time.sleep(180*60)
                
            except:
                if weather_engine_pred is None:
                    print(traceback.format_exc())
        
        talk_session.close()
        return
         
    def writeToDatabase(self, weather_engine_pred, talk_session, data):
        self.data = data
        weather_engine_pred.execute("TRUNCATE TABLE dublinbikes.weather_prediction")
        weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
 
        for i in self.data["list"]: 
            weekday_1 = "0"
            weekend_1 = "0"
            
            rain = 0
            
            now = datetime.datetime.now()
             
            date = i["dt"]
            day = time.strftime('%A', time.localtime(date))
            hour= time.strftime('%H', time.gmtime(date))
            day_decimal = time.strftime('%w', time.localtime(date))
             
            if day in weekdays:
                weekday_1 ="1"
            else:
                weekend_1 ="1"
            
                
            description=i["weather"][0]["description"]
       
            if description == "light intensity drizzle" \
                or description == "light intensity drizzle rain" \
                or description == "light intensity shower rain" \
                or description == "light rain" \
                or description == "shower rain":
                rain = 1
             
            else:
                rain = 0
             
             
             
       
            weather = Weather(humidity=i["main"]["humidity"],
                                          temp=i["main"]["temp"],
                                          temp_max=i["main"]["temp_max"],
                                          temp_min=i["main"]["temp_min"],
                                          description=i["weather"][0]["description"],
                                          icon=i["weather"][0]["icon"],
                                          main_description=i["weather"][0]["main"],
                                          day =day,
                                          weekday=weekday_1,
                                          weekend = weekend_1,
                                          hour=hour,
                                          day_num =day_decimal,
                                          rain = rain,
                                          timeDate=str(now))
                                            
                                      
         
            talk_session.add(weather)
            talk_session.commit()
               
        return