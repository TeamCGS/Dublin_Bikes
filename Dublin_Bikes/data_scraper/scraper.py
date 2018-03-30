import json
import requests
from sqlalchemy import Column, Integer, String, Float, Boolean
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import datetime
import time 

from dataScraperBase import data_Base


class Static(data_Base):
    """
    Create an Stations table
    """
    __tablename__ = 'Stations'
    
    address = Column(String (100), nullable=False)
    available_bike_stands = Column(Integer, nullable=False)
    available_bikes = Column(Integer, nullable=False)
    banking = Column(Boolean, nullable=False)
    bike_stands = Column(Integer, nullable=False)
    bonus = Column(Boolean, nullable=False)
    contract_name = Column(String (100), nullable=False)
    last_update = Column(Integer, nullable=False)
    name = Column(String (100), nullable=False)
    number = Column(Integer, primary_key=True, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    status = Column(String (100), nullable=False)
    timeDate = Column(String (100), primary_key=True, nullable=False)


    def getData(self):
        
               
        engine = create_engine('mysql+mysqlconnector://CGSdatabase:password@dublinbikes.ctaptplk7c5t.eu-west-1.rds.amazonaws.com/dublinbikes', convert_unicode=True)
        Session = sessionmaker(bind=engine)
        session = Session()         
        data_Base.metadata.create_all(bind=engine)
        
        for i in range(0,5,1):
            #try:
                
                
            APIKEY = "e5affb7993b5897408c7a362ae50fa900d6c593e"
            NAME = "Dublin"
            STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
            r = requests.get(STATIONS_URI, params={"apiKey": APIKEY,
                                                   "contract": NAME})
            data = r.json()
            #pprint(data)
            
            self.writeToDatabase(session,data)
            print("should have filled database")
            #time.sleep(5*60)
           
            #except:
             #   if engine is None:
              #      print(traceback.format_exc())
        
        #session.close()
        return
    
     
    def writeToDatabase(self,session,data1): 
        self.data = data1
        print("vdfjvwjvfkwhkfbew",self.data)
        print("entering write to database")     
        for i in self.data:
            
            now = datetime.datetime.now() 
            print(i)
            station = Static(address=i["address"],
                                        available_bike_stands=i["available_bike_stands"],
                                        available_bikes=i["available_bikes"],
                                        banking=i["banking"],
                                        bike_stands=i["bike_stands"],
                                        bonus=i["bonus"],
                                        contract_name=i["contract_name"],
                                        last_update=i["last_update"],
                                        name=i["name"],
                                        number=i["number"],
                                        lat=i["position"]["lat"],
                                        lng=i["position"]["lng"],
                                        status=i["status"],
                                        timeDate=now)
            
            print("++++++")
            session.add(station)
            session.commit()
            print("------")
        #session.close()
            
        return 