from vehicle_states import *
from event_handler import *
from stopwatch import Stopwatch

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
        self.tripRideTimeOnBoot     = 0
        self.rideTimeOnboot         = 0
        self.rideTimeInitialization = 0

        #initialze
        self.loadData()
        self.computeTripDistance()
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
        print('tripOdoOffset: ', str(self.tripOdoOffset))
        print('tripSpeedInitial: ', str(self.tripAverageSpeed))
        print('Average Speed On Boot: ', str(self.averageSpeed))
        print('Max Speed On Boot: ', str(self.maxSpeed))

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
        self.tripDistance = self.odometer - self.tripOdoOffset
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
        self.rideTimeOnboot = self.odoReading / self.averageSpeed
        self.tripRideTimeOnboot = self.tripDistance / self.tripAverageSpeed
        self.initialRideTimeStatus = 1
        print('InitialRideTime: ', str(self.initialRideTime))
        print('initialTripRideTime: ', str(self.initialTripRideTime))
        
        vehicleReadings.odoReading += self.updateOdoReading()

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
        self.averageSpeed = self.odoReading / (self.rideTimeOnboot + self.stopwatch.duration/3600)
        # print('Total Distance: ', str(self.odometer))
        # print('Ride Time: ', str(self.rideTime))
        # print('Average Speed: ', str(self.averageSpeed))

        self.computeTripDistance()
        self.tripRideTime = (self.stopwatch.duration / 3600) + self.tripRideTimeOnboot - self.tripRideTimeOffset
        self.tripAverageSpeed = self.tripDistance / self.tripRideTime
        # print('initialTripRideTime: ', str(self.initialTripRideTime))
        # print('tripRideTime: ', str(self.tripRideTime))
        # print('Trip Average Speed: ', str(self.tripAverageSpeed))
        # print('Trip Average Speed: ', str(self.tripAverageSpeed))
        vehicleReadings.averageSpeeds(self.odoAverageSpeed, self.tripAverageSpeed)

    def resetTrip(self):
        tripReset = {
            'tripDistanceOffsetOnBoot': self.odoReading,
            'averageTripSpeedOnBoot': 0
        }
        with open('trip.json', 'w') as f:  # writing JSON object
            json.dump(tripReset, f)
        self.tripOdoOffset = self.odometer
        self.tripDistance = 0
        self.tripRideTimeOffset = self.stopwatch.duration/3600 + self.tripRideTimeOnboot
        vehicleReadings.distances(self.odoReading, self.tripDistance) 
        publishOdometer(self.odometer, self.tripOdo)