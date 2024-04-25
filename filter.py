import pandas as pd
import graphviz as gv
import numpy as np
import time
from haversine import haversine, haversine_vector

start = time.time()

df = pd.read_csv('flights_final.csv')
flights = []
codes = []
table = {'Airport 1': [],
         'Airport 2': [],
         'Distance': []
         }
airports = {'Code': [],
            'City': [],
            'Country': [],
            'Latitude': [],
            'Longitude': []
            }

for index, row in df.iterrows():
    source = row['Source Airport Code']
    destination = row['Destination Airport Code']
    if {source, destination} not in flights:
        lat1 = row['Source Airport Latitude']
        long1 = row['Source Airport Longitude']
        lat2 = row['Destination Airport Latitude']
        long2 = row['Destination Airport Longitude']
        distance = haversine((lat1, long1), (lat2, long2))
        table['Airport 1'].append(source)
        table['Airport 2'].append(destination)
        table['Distance'].append(distance)
        flights.append({source, destination})
    if source not in codes:
        name = row['Source Airport Name']
        city = row['Source Airport City']
        country = row['Source Airport Country']
        latitude = row['Source Airport Latitude']
        longitude = row['Source Airport Longitude']
        airports['Code'].append(source)
        airports['City'].append(city)
        airports['Country'].append(country)
        airports['Latitude'].append(latitude)
        airports['Longitude'].append(longitude)
        codes.append(source)
    if destination not in codes:
        name = row['Destination Airport Name']
        city = row['Destination Airport City']
        country = row['Destination Airport Country']
        latitude = row['Destination Airport Latitude']
        longitude = row['Destination Airport Longitude']
        airports['Code'].append(destination)
        airports['City'].append(city)
        airports['Country'].append(country)
        airports['Latitude'].append(latitude)
        airports['Longitude'].append(longitude)
        codes.append(destination)

distance_df = pd.DataFrame(table)
distance_df.to_csv('distance.csv', index=False)

airports_df = pd.DataFrame(airports)
airports_df.to_csv('airports.csv', index=False)

end = time.time()

print(end-start)