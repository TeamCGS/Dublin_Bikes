import json
import requests
from pprint import pprint
from sqlalchemy.orm import sessionmaker


def main():
    
    from Dublin_Bikes import engine
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    APIKEY = "e5affb7993b5897408c7a362ae50fa900d6c593e"
    NAME = "Dublin"
    STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
    r = requests.get(STATIONS_URI, params={"apiKey": APIKEY,
                                           "contract": NAME})
    data = r.json()
    pprint(data)
    
    
    #r = requests.get("{}/{}".format(STATIONS_URI, 99),
                     #params={"apiKey": APIKEY, "contract": NAME})
    #pprint(json.loads(r.text))
    
   
    from Dublin_Bikes.models import Static
    
    for i in data:
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
                                    status=i["status"])
        session.add(station)
        session.commit()
    
    session.close()

main()