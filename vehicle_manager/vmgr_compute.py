from vehicle_states import *
from event_handler import *
from stopwatch import Stopwatch
import json

class VehicleInfoCalculator:
    def __init__(self):
        # inputs
        self.odoReading             = 0
        self.speedReading           = 0

        # outputs
        self.tripDistance           = 0
        self.maxSpeed               = 0
        self.odoAverageSpeed        = 0
        self.tripAverageSpeed       = 0

        #intermediates
        self.tripRideTime           = 0
        self.tripRideTimeOffset     = 0
        self.tripRideTimeOnboot     = 0
        self.rideTimeOnboot         = 0     # hr
        self.rideTimeInitialization = False # False means ride-time has not been initialized

        #initialze
        self.loadData()
        self.stopwatch = Stopwatch()
        self.subscribeToEvents()
    
    # 
    # Load data from json file on bootup
    # 
    def loadData(self):
        tripData = {}
        speed = {}
        with open('trip.json', 'r') as f:
            tripData = json.load(f)
        self.tripOdoOffset = tripData['tripDistanceOffsetOnBoot']
        self.tripAverageSpeed = tripData['averageTripSpeedOnBoot']

        with open('speed.json', 'r') as f:
            speed = json.load(f)
            self.averageSpeed = speed['odoAverageSpeedOnBoot']
            self.maxSpeed = speed['maxSpeedOnBoot']
        
        vehicleReadings.maxSpeed(self.maxSpeed)
        vehicleReadings.averageSpeeds(self.averageSpeed, self.tripAverageSpeed)
        # print('tripOdoOffset: ', str(self.tripOdoOffset))
        # print('tripSpeedInitial: ', str(self.tripAverageSpeed))
        # print('Average Speed On Boot: ', str(self.averageSpeed))
        # print('Max Speed On Boot: ', str(self.maxSpeed))

    # 
    # Subscribe to vehicleReading events which will be provided by the CAN module
    # 
    def subscribeToEvents(self):
        vehicleReadings.odoReading += self.initializeRideTime
        vehicleReadings.speedReading += self.updateSpeedReading
        vehicleEvents.onTripReset += self.resetTrip
    # 
    # update the member odoReading
    # and then call methods that use odoReading
    # 
    def updateOdoReading(self, value):
        self.odoReading = value
        self.computeTripDistance()
        self.computeAverageSpeeds()
    
    # 
    # update the member speedReading
    # and then call methods that use speedReading
    # 
    def updateSpeedReading(self, value):
        self.speedReading = value
        
        if(self.speedReading > 1):
            if(not self.stopwatch.running):
                self.stopwatch.start()
        else:
            if(self.stopwatch.running):
                self.stopwatch.stop()
                # self.currentRideTime = self.stopwatch.duration
        self.computeMaxSpeed()
        
    # 
    # 
    def computeTripDistance(self):
        self.tripDistance = self.odoReading - self.tripOdoOffset
        vehicleReadings.distances(self.odoReading, self.tripDistance)
    
    def computeMaxSpeed(self):
        if self.speedReading > self.maxSpeed:
            self.maxSpeed = self.speedReading
            vehicleReadings.maxSpeed(self.maxSpeed)

    # 
    # [ Description ]
    # Initialize overall-ride-time and trip-ride-time
    # 
    # [Outputs]
    # Overall-Ride-Time = Odo-Reading / Odo-Average-Speed
    # Trip-Ride-Time = Trip-Distance / Trip-Average-Speed
    # 
    # [Inputs]
    # Odo-Reading comes from CAN
    # Odo-Average-Speed initially comes from the json file
    # Trip-Distance should be computed before this method is called
    # Trip-Average-Speed initially comes from the json file
    # 
    def initializeRideTime(self, value):
        if(self.rideTimeInitialization):
            return
        
        self.odoReading = value
        self.computeTripDistance()

        if (self.averageSpeed != 0):
            self.rideTimeOnboot = int(self.odoReading / self.averageSpeed)

        # print("TripDistance: ", str(self.tripDistance), ": TripAvSpeed: ", str(self.tripAverageSpeed))
        if(self.tripAverageSpeed != 0):
            self.tripRideTimeOnboot = int(self.tripDistance / self.tripAverageSpeed)
        
        # print('InitialRideTime: ', str(self.rideTimeOnboot))
        # print('initialTripRideTime: ', str(self.tripRideTimeOnboot))
        self.rideTimeInitialization = True

        vehicleReadings.odoReading += self.updateOdoReading

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
    def computeAverageSpeeds(self):
        self.averageSpeed = int(self.odoReading / (self.rideTimeOnboot + self.stopwatch.duration/3600))
        # print('Total Distance: ', str(self.odometer))
        # print('Ride Time: ', str(self.rideTime))
        # print('Average Speed: ', str(self.averageSpeed))

        self.computeTripDistance()
        self.tripRideTime = (self.stopwatch.duration / 3600) + self.tripRideTimeOnboot - self.tripRideTimeOffset

        if((self.tripDistance != 0) and (self.tripRideTime != 0)):
            self.tripAverageSpeed = int(self.tripDistance / self.tripRideTime)
        else:
            self.tripAverageSpeed = 0
        # print('initialTripRideTime: ', str(self.initialTripRideTime))
        # print('tripRideTime: ', str(self.tripRideTime))
        # print('Trip Average Speed: ', str(self.tripAverageSpeed))
        # print('Trip Average Speed: ', str(self.tripAverageSpeed))
        # print("OdoReading: ", str(self.odoReading),": rideTimeOnboot: ", str(self.rideTimeOnboot),": tripRideTimeOnboot: ", str(self.tripRideTimeOnboot), ": tripRideTimeOffset: ", str(self.tripRideTimeOffset) )
        vehicleReadings.averageSpeeds(self.averageSpeed, self.tripAverageSpeed)

    def resetTrip(self):
        self.tripRideTimeOffset = self.stopwatch.duration/3600 + self.tripRideTimeOnboot
        self.tripOdoOffset = self.odoReading
        self.tripDistance = 0

        tripReset = {
            'tripDistanceOffsetOnBoot': self.tripOdoOffset,
            'averageTripSpeedOnBoot': 0
        }
        with open('trip.json', 'w') as f:  # writing JSON object
            json.dump(tripReset, f)
        
        vehicleReadings.distances(self.odoReading, self.tripDistance) 
        publishOdometer(self.odometer, self.tripOdo)