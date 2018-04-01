#!/usr/bin/env python

from sqlalchemy import create_engine
engine = create_engine('mysql://CGSdatabase:password@dublinbikes.ctaptplk7c5t.eu-west-1.rds.amazonaws.com/dublinbikes')

result = engine.execute("SELECT address, available_bike_stands, available_bikes, banking, bike_stands, last_update, name, Static_Data.number, lat, lng, status, timeDate  FROM Static_Data JOIN Stations ON Static_Data.number = Stations.number")

for row in result:
    print("username:", row['bike_stands'] , row['banking'], row['address'])

    