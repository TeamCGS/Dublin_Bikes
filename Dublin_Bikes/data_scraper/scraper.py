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

#Commented out as enough data collected
# class JoinedTables(data_Base):
#     __tablename__ = 'JoinedTable2'
#     
#     number = Column(Integer, primary_key=True, nullable=False)
#     name = Column(String (100), nullable=False)
#     address = Column(String (100), nullable=False,primary_key=True)
#     lat = Column(Float, nullable=False)
#     lng = Column(Float, nullable=False)
#     available_bike_stands = Column(Integer, nullable=False)
#     available_bikes = Column(Integer, nullable=False)
#     banking = Column(Boolean, nullable=False)
#     bike_stands = Column(Integer, nullable=False)
#     last_update = Column(Integer, nullable=False)
#     number = Column(Integer, primary_key=True, nullable=False)
#     status = Column(String (100), nullable=False)
#     timeDate = Column(String (100), primary_key=True, nullable=False)
    
    
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
     
        new_engine = create_engine('mysql+mysqlconnector://CGSdatabase:password@dublinbikes.ctaptplk7c5t.eu-west-1.rds.amazonaws.com/dublinbikes', convert_unicode=True)
        Session = sessionmaker(bind=new_engine)
        session = Session()         
        data_Base.metadata.create_all(bind=new_engine) # Creates the tables in the database 
        
         
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


    def getData(self,setOfNumbers):
        self.numbers = setOfNumbers
        
        #Connecting to the database and initalising a session.
        new_engine = create_engine('mysql+mysqlconnector://CGSdatabase:password@dublinbikes.ctaptplk7c5t.eu-west-1.rds.amazonaws.com/dublinbikes', convert_unicode=True)
        Session = sessionmaker(bind=new_engine)
        session = Session()         
        data_Base.metadata.create_all(bind=new_engine) # Creates the tables in the database 
        
        
        # initialising a boolean to true. This is used in the while funciton below to initalise the database.
        bool = True
        while True:
            try:
                APIKEY = "e5affb7993b5897408c7a362ae50fa900d6c593e"
                NAME = "Dublin"
                STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
                r = requests.get(STATIONS_URI, params={"apiKey": APIKEY,
                                                       "contract": NAME})
                data = r.json()
                #pprint(data)
                
                while(bool):
                    # this will only run once and its purpose is to initalise the database at the beginning. Otherwise would get an error as trying to update nothing.
                    for i in data:
                        now = datetime.datetime.now()
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
                        bool=False
                #print("just before write to database")
                self.writeToDatabase(new_engine,session,data,self.numbers) # calling the method below to update the database 
                #print("after write to database")
                time.sleep(5*60)
           
            except:
                if new_engine is None:
                    print(traceback.format_exc())
        
        session.close()
        return
    



    def writeToDatabase(self,new_engine,session,data1, numberSet): 
        
        self.data = data1
        self.numberIds = numberSet
       
        for i in self.data:
            
            now = datetime.datetime.now()
            if i["number"] not in self.numberIds:
                

                self.numberIds.add(i["number"])
                
                
                staticData = ReallyStatic(number=i["number"],
                                      name=i["name"],
                                      address=i["address"],
                                      lat=i["position"]["lat"],
                                      lng=i["position"]["lng"])
            
                   
                updated_available_bike_stands = str(i["available_bike_stands"])
                updated_available_bikes = str(i["available_bikes"])
                updated_banking = str(i["banking"])
                updated_bike_stands = str(i["bike_stands"])
                updated_last_update = str(i["last_update"])
                updated_number = str(i["number"])
                updated_status = str(i["status"])
                updated_timeDate=str(now)
                
                new_engine.execute("UPDATE dublinbikes.Stations SET available_bike_stands= %s, available_bikes = %s, banking = %s, bike_stands = %s, last_update= %s, status = %s, timeDate = %s   WHERE number = %s",(updated_available_bike_stands, updated_available_bikes, updated_banking, updated_bike_stands,updated_last_update, updated_status, updated_timeDate, updated_number))
                # this query updates each of the values in the dynamic database.
                session.add(staticData)
                session.commit()
                
            else:
                
                now_time = datetime.datetime.now()
                #need to convert the data to strings so they can be implemented in the sql query
                
                updated_available_bike_stands = str(i["available_bike_stands"])
                updated_available_bikes = str(i["available_bikes"])
                updated_banking = str(i["banking"])
                updated_bike_stands = str(i["bike_stands"])
                updated_last_update = str(i["last_update"])
                updated_number = str(i["number"])
                updated_status = str(i["status"])
                updated_timeDate=str(now_time)
                

                new_engine.execute("UPDATE dublinbikes.Stations SET available_bike_stands= %s, available_bikes = %s, banking = %s, bike_stands = %s, last_update= %s, status = %s, timeDate = %s   WHERE number = %s",(updated_available_bike_stands, updated_available_bikes, updated_banking, updated_bike_stands,updated_last_update, updated_status, updated_timeDate, updated_number))
                # this query updates each of the values in the dynamic database.
            
        return 
    
# commented out as enough data collected  
#         def joiningTable(self,session,e):
#         #print("joing table") 
#         engine = e
#         result = engine.execute("SELECT address, available_bike_stands, available_bikes, banking, bike_stands, last_update, name, Static_Data.number, lat, lng, status, timeDate  FROM Stations JOIN Static_Data ON Static_Data.number = Stations.number")
#         for x in result:
#             
#             joined_tables = JoinedTables(address=x[0],
#                                             available_bike_stands= int(x[1]),
#                                             available_bikes=int(x[2]),
#                                             banking=bool(x[3]),
#                                             bike_stands=int(x[4]),
#                                             last_update=int(x[5]),
#                                             name=x[6],
#                                             number=int(x[7]),
#                                             lat=float(x[8]),
#                                             lng=float(x[9]),
#                                             status=x[10],
#                                             timeDate=x[11])
#             
#             
#             session.add(joined_tables)
#             
#             session.commit()
#            
#         
#           
#         return

        