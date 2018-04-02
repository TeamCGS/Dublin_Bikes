import json
import requests
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import datetime
import time 
from dataScraperBase import data_Base
import csv
from werkzeug.contrib.profiler import available

class ReallyStatic(data_Base):
    """
    Create a static data table
    """
    __tablename__ = 'Static_Data'
    
    number = Column(Integer, primary_key=True, nullable=False)
    name = Column(String (100), nullable=False)
    address = Column(String (100), nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
   
   
   
    
    def getData(self):
        
        engine = create_engine('mysql+mysqlconnector://CGSdatabase:password@dublinbikes.ctaptplk7c5t.eu-west-1.rds.amazonaws.com/dublinbikes', convert_unicode=True)
        Session = sessionmaker(bind=engine, expire_on_commit=False)
        session = Session()  
        data_Base.metadata.create_all(bind=engine)
        
        numberId = set()
        file = open('Dublin.csv', 'r')
        reader = csv.reader(file)
        
        for row in reader:
            numberId.add(int(row[0]))
            now = datetime.datetime.now() 
            
            staticData = ReallyStatic(number=row[0],
                                      name=row[1],
                                      address=row[2],
                                      lat=row[3],
                                      lng=row[4])
            
            session.add(staticData)
            session.commit()   
        session.close()
       
        return numberId


        
class JoinedTables(data_Base):
    __tablename__ = 'JoinedTable'
    
    number = Column(Integer, primary_key=True, nullable=False)
    name = Column(String (100), nullable=False)
    address = Column(String (100), nullable=False,primary_key=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    available_bike_stands = Column(Integer, nullable=False)
    available_bikes = Column(Integer, nullable=False)
    banking = Column(Boolean, nullable=False)
    bike_stands = Column(Integer, nullable=False)
    last_update = Column(Integer, nullable=False)
    number = Column(Integer, primary_key=True, nullable=False)
    status = Column(String (100), nullable=False)
    timeDate = Column(String (100), primary_key=True, nullable=False)
    
    
    
        
class Dynamic(data_Base):
    """
    Create a dynamic data table
    """
    __tablename__ = 'Stations'
    
    
    available_bike_stands = Column(Integer, nullable=False)
    available_bikes = Column(Integer, nullable=False)
    banking = Column(Boolean, nullable=False)
    bike_stands = Column(Integer, nullable=False)
    last_update = Column(Integer, nullable=False)
    number = Column(Integer, primary_key=True, nullable=False)
    status = Column(String (100), nullable=False)
    timeDate = Column(String (100), primary_key=True, nullable=False)


    def getData(self, setOfNumbers):
               
        engine = create_engine('mysql+mysqlconnector://CGSdatabase:password@dublinbikes.ctaptplk7c5t.eu-west-1.rds.amazonaws.com/dublinbikes', convert_unicode=True)
        Session = sessionmaker(bind=engine)
        session = Session()         
        data_Base.metadata.create_all(bind=engine)
        
        while True:
            try:
                
                APIKEY = "e5affb7993b5897408c7a362ae50fa900d6c593e"
                NAME = "Dublin"
                STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
                r = requests.get(STATIONS_URI, params={"apiKey": APIKEY,
                                                       "contract": NAME})
                data = r.json()
                #pprint(data)
                
                self.writeToDatabase(engine,session,data,setOfNumbers)
                self.joiningTable(session,engine)
                time.sleep(1*10)
           
            except:
                if engine is None:
                    print(traceback.format_exc())
        
        session.close()
        return
    



    def writeToDatabase(self,engine,session,data1,numberSet): 
        
        self.data = data1
        self.numberIds = numberSet
        #print("entering write to database")     
        engine.execute("TRUNCATE TABLE dublinbikes.Stations") #removes exsisting data from the database
        
        for i in self.data:
            #print(i["number"])
            now = datetime.datetime.now()
            if i["number"] not in self.numberIds:
                self.numberIds.add(i["number"])
                
            
                staticData = ReallyStatic(number=i["number"],
                                      name=i["name"],
                                      address=i["address"],
                                      lat=i["position"]["lat"],
                                      lng=i["position"]["lng"])
            
                    
                station = Dynamic(available_bike_stands = i["available_bike_stands"],
                                  available_bikes = i["available_bikes"],
                                  banking = i["banking"],
                                  bike_stands = i["bike_stands"],
                                  last_update = i["last_update"],
                                  number = i["number"],
                                  status = i["status"],
                                  timeDate=now)
                
                session.add(staticData)
                session.add(station)
                session.commit()
                
            
            else:
                
                station = Dynamic(available_bike_stands = i["available_bike_stands"],
                                  available_bikes = i["available_bikes"],
                                  banking = i["banking"],
                                  bike_stands = i["bike_stands"],
                                  last_update = i["last_update"],
                                  number = i["number"],
                                  status = i["status"],
                                  timeDate=now)
                
                session.add(station)
                session.commit()
            
        return 
    
    def joiningTable(self,session,e):
        #print("joing table") 
        engine = e
        result = engine.execute("SELECT address, available_bike_stands, available_bikes, banking, bike_stands, last_update, name, Static_Data.number, lat, lng, status, timeDate  FROM Stations JOIN Static_Data ON Static_Data.number = Stations.number")
        for x in result:
            
            joined_tables = JoinedTables(address=x[0],
                                            available_bike_stands= int(x[1]),
                                            available_bikes=int(x[2]),
                                            banking=bool(x[3]),
                                            bike_stands=int(x[4]),
                                            last_update=int(x[5]),
                                            name=x[6],
                                            number=int(x[7]),
                                            lat=float(x[8]),
                                            lng=float(x[9]),
                                            status=x[10],
                                            timeDate=x[11])
            
            
            session.add(joined_tables)
            
            session.commit()
           
        
          
        return
        

            

        