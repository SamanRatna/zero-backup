from vehicle_states import *
from event_handler import *
# from stopwatch import Stopwatch
import json
import math

FILE_TRIP = '/etc/yatri/trip.json'
FILE_SPEED = '/etc/yatri/speed.json'
MILEAGE_PETROL = 25             # km per litre of petrol
MILEAGE_BATTERY = 2             # km per Ah
UNIT_COST_OF_PETROL = 100       # NRs
UNIT_COST_OF_AH     = 1.4       # NRs

class VehicleInfoCalculator:
    def __init__(self):
        # inputs
        self.odoReading             = None
        self.speedReading           = 0
        self.tractionHours          = None

        # outputs
        self.tripDistance           = 0
        self.maxSpeed               = 0
        self.tripMaxSpeed           = 0
        self.averageSpeed           = 0
        self.tripAverageSpeed       = 0
        self.fuelSavings            = 0

        #persistency
        self.tripDistanceOffset     = 0
        self.tripTimeOffset         = 0

        #intermediates
        self.tripRideTime           = 0
        self.tripRideTimeOffset     = 0
        self.tripRideTimeOnboot     = 0
        self.rideTimeOnboot         = 0     # hr
        self.rideTimeInitialization = False # False means ride-time has not been initialized

        #initialze
        self.subscribeToEvents()
        self.loadData()
        print('VehicleInfoCalculator initialized.')
    
    # 
    # Load data from json file on bootup
    # 
    def loadData(self):
        tripData = {}
        speed = {}
        try:
            with open(FILE_TRIP, 'r') as f:
                tripData = json.load(f)
            self.tripDistanceOffset = tripData['tripDistanceOffsetOnBoot']
            self.tripTimeOffset = tripData['tripTimeOffsetOnBoot']
        except Exception as error:
            print(error)

        try:
            with open(FILE_SPEED, 'r') as f:
                speed = json.load(f)
                self.maxSpeed = speed['maxSpeedOnBoot']
                self.tripMaxSpeed = speed['tripMaxSpeedOnBoot']
        except Exception as error:
            print(error)
        
        vehicleReadings.maxSpeed(self.maxSpeed)
        vehicleReadings.tripMaxSpeed(self.tripMaxSpeed)

    # 
    # Subscribe to vehicleReading events which will be provided by the CAN module
    # 
    def subscribeToEvents(self):
        vehicleEvents.guiReady += self.onGUIReady
        vehicleReadings.distancehour += self.initializeRideTime
        vehicleReadings.speedReading += self.updateSpeedReading
        vehicleEvents.onTripReset += self.resetTrip
        vehicleEvents.bluetoothStatus += self.onBluetoothStatusChange
    # 
    # update the member odoReading
    # and then call methods that use odoReading
    # 
    def updateOdoReading(self, odometer, tractionHour):
        if(self.odoReading == None):
            self.odoReading = 0
        self.tractionHours = tractionHour
        self.computeTripDistance(odometer)

        if(abs(self.odoReading - odometer) > 0.1):
            vehicleReadings.distances(odometer, self.tripDistance)
        self.odoReading = odometer

        self.computeAverageSpeeds(odometer, tractionHour)
        self.calculateFuelSavings(self.odoReading)
    # 
    # update the member speedReading
    # and then call methods that use speedReading
    # 
    def updateSpeedReading(self, value):
        self.speedReading = value
        self.computeMaxSpeed(value)

    def computeTripDistance(self, newOdoReading):
        oldTripDistance = 0
        if(self.tripDistance != None):
            oldTripDistance = self.tripDistance


        newTripDistance = newOdoReading - self.tripDistanceOffset

        if((newTripDistance - oldTripDistance) > 0 ):
            self.tripDistance = newTripDistance
    
    def computeMaxSpeed(self, newSpeed):
        flagNewData = False
        # compute overall max speed
        if math.floor(newSpeed) > self.maxSpeed:
            self.maxSpeed = math.floor(newSpeed)
            vehicleReadings.maxSpeed(self.maxSpeed)
            flagNewData = flagNewData | True

        # compute trip max speed
        if math.floor(newSpeed) > self.tripMaxSpeed:
            self.tripMaxSpeed = math.floor(newSpeed)
            vehicleReadings.tripMaxSpeed(self.tripMaxSpeed)
            flagNewData = flagNewData | True
        
        # if there's new MAX_SPEED or TRIP_MAX_SPEED,
        # save the data to persistency
        if(flagNewData):
            self.saveMaxSpeedsToPersistency(self.maxSpeed, self.tripMaxSpeed)

    def initializeRideTime(self, odometer, tractionHour):
        if(self.rideTimeInitialization):
            return
        
        self.odoReading = odometer
        self.computeTripDistance(odometer)

        vehicleReadings.distances(self.odoReading, self.tripDistance)
        
        self.rideTimeInitialization = True

        vehicleReadings.distancehour += self.updateOdoReading

    # 
    # [Description]
    # Compute overall-average-speed and trip-average-speed
    # 
    # [Outputs]
    # overall-average-speed = odo-reading / (ride-time-onboot + current-ride-time)
    # trip-average-speed = trip-distance / (trip-ride-time-onboot - trip-ride-time-offset + current-ride-time)
    # 
    # [Inputs]
    # odo-reading comes from CAN
    # ride-time-onboot comes from the json file
    # current-ride-time is calculated using a stopwatch
    # trip-distance should be computed
    # 
    def computeAverageSpeeds(self, distance, time):
        tempAverageSpeed = self.averageSpeed
        newAverageSpeed = math.floor(distance / time)

        tempTripAverageSpeed = self.tripAverageSpeed
        if(int(time - self.tripTimeOffset) == 0):
            newTripAverageSpeed = 0
        else:
            newTripAverageSpeed = math.floor((distance - self.tripDistanceOffset) / (time - self.tripTimeOffset))

        if((newAverageSpeed != tempAverageSpeed) or (newTripAverageSpeed != tempTripAverageSpeed)):
            self.averageSpeed = newAverageSpeed
            self.tripAverageSpeed = newTripAverageSpeed
            vehicleReadings.averageSpeeds(self.averageSpeed, self.tripAverageSpeed)

    def resetTrip(self):
        self.tripDistanceOffset = self.odoReading
        self.tripTimeOffset = self.tractionHours
        self.tripDistance = 0

        tripReset = {
            'tripDistanceOffsetOnBoot': self.tripDistanceOffset,
            'tripTimeOffsetOnBoot': self.tractionHours
        }
        with open(FILE_TRIP, 'w') as f:  # writing JSON object
            json.dump(tripReset, f)

        vehicleReadings.distances(self.odoReading, self.tripDistance)

        # set trip max speed to zero
        self.tripMaxSpeed = 0
        self.saveMaxSpeedsToPersistency(self.maxSpeed, self.tripMaxSpeed)
        vehicleReadings.tripMaxSpeed(self.tripMaxSpeed)

    def saveMaxSpeedsToPersistency(self, maxSpeed, tripMaxSpeed):
        maxSpeeds = {
            "maxSpeedOnBoot" : maxSpeed,
            "tripMaxSpeedOnBoot": tripMaxSpeed
        }
        with open(FILE_SPEED, 'w') as f:  # writing JSON object
            json.dump(maxSpeeds, f)

    def onBluetoothStatusChange(self, state):
        print('Bluetooth Status Changed.')
        if(state == 'SERVICES_READY'):
            vehicleReadings.maxSpeed(self.maxSpeed)
            vehicleReadings.tripMaxSpeed(self.tripMaxSpeed)
            vehicleReadings.averageSpeeds(self.averageSpeed, self.tripAverageSpeed)
            if(self.odoReading != None and self.tripDistance != None):
                vehicleReadings.distances(self.odoReading, self.tripDistance)

    def onGUIReady(self):
        vehicleReadings.maxSpeed(self.maxSpeed)
        vehicleReadings.tripMaxSpeed(self.tripMaxSpeed)
        vehicleReadings.averageSpeeds(self.averageSpeed, self.tripAverageSpeed)
        if(self.odoReading != None and self.tripDistance != None):
            vehicleReadings.distances(self.odoReading, self.tripDistance)
        vehicleReadings.fuelSavings(self.fuelSavings)

    def calculateFuelSavings(self, distance):
        costOfPetrol = distance / MILEAGE_PETROL * UNIT_COST_OF_PETROL
        costOfBattery = distance / MILEAGE_BATTERY * UNIT_COST_OF_AH
        self.fuelSavings = int(costOfPetrol - costOfBattery)
        vehicleReadings.fuelSavings(self.fuelSavings)
