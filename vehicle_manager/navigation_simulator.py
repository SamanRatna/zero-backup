import eel
import json
import threading
import time
from event_handler import *

navigation = False
@eel.expose
def updateRoute(data):
    try:
        with open('route.json', 'w') as f:
            json.dump(data,f)
    except ( ) as error:
        print('Update Route Exception')
        print(error)

@eel.expose
def startNavigation():
    simulateRoute()

def simulateRoute():
    route = []
    try:
        with open('route.json', 'r') as f:
            route = json.load(f)

        for data in route:
            time.sleep(0.5)
            vehicleReadings.gpsLocation(data[1], data[0])

    except () as error:
        print(error)
    

