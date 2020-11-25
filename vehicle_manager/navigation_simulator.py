import eel
import json
import threading
import time
from event_handler import *
import math

navigation = False
@eel.expose
def updateRoute(data):
    try:
        with open('route.json', 'w') as f:
            json.dump(data,f)
    except ( ) as error:
        print('Update Route Exception')
        print(error)

# @eel.expose
# def startNavigation():
#     simulateRoute()
def simulateRoute(event):
    if(event != True):
        return
    route = []
    pastData = None
    currentData = [0,0,0] #latitude, longitude, bearing
    try:
        with open('route.json', 'r') as f:
            route = json.load(f)

        # # for data in route:
        # for data in route['legs'][0]['steps'][0]['geometry']['coordinates']:
        #     time.sleep(1)
        #     currentData = [data[1], data[0], 0]
        #     # vehicleReadings.gpsLocation(data[1], data[0])
        #     # input('Waiting for user input.')
        #     if(pastData != None):
        #         currentData[2] = calculateHeading(pastData, currentData)
        #     pastData = currentData
        #     vehicleReadings.heading(currentData)
                # for data in route:
        for data in route['legs'][0]['steps']:
            for items in data['geometry']['coordinates']:
                time.sleep(1)
                currentData = [items[1], items[0], 0]
                # vehicleReadings.gpsLocation(data[1], data[0])
                # input('Waiting for user input.')
                if(pastData != None):
                    currentData[2] = calculateHeading(pastData, currentData)
                pastData = currentData
                vehicleReadings.heading(currentData)

    except () as error:
        print(error)
    

def calculateHeading(location_a, location_b):
    lat_a = location_a[0]
    lon_a = location_a[1]
    lat_b = location_b[0]
    lon_b = location_b[1]
    delta_lon = lon_b - lon_a
    
    x = math.cos(lat_b) * math.sin(delta_lon)
    y = math.cos(lat_a) * math.sin(lat_b) - math.sin(lat_a)*math.cos(lat_b)*math.cos(delta_lon)
    heading = math.atan2(x,y)
    heading = math.degrees(heading)
    print('Heading: ', heading)
    # vehicleReadings.heading(heading)
    return(heading)

# vehicleEvents.onNavigation += simulateRoute
