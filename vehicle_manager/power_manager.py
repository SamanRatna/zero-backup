from event_handler import *
import threading
from gpio_manager import RepeatableTimer
import subprocess
import json
from datetime import datetime

COST_FACTOR = 1.2
CHARGE_SAVINGS_FILE = 'charge-savings.json'
MAX_DATA_COUNT = 30

class PowerManager():
    def __init__(self):
        self.standState = 0
        self.socOnChargeStart = None
        self.socOnChargeEnd = None
        self.chargeSavingsData = []
        try:
            with open(CHARGE_SAVINGS_FILE, 'r') as f:
                self.chargeSavingsData = json.load(f)

        except (OSError, json.decoder.JSONDecodeError) as error:
            print(error)

        vehicleEvents.onStandSwitch += self.updateStandState
        vehicleEvents.onUserInteraction += self.uiMonitor
        vehicleEvents.bikeOff += self.onBikeOff
        vehicleEvents.bikeOn += self.onBikeOn
        vehicleEvents.charging += self.onCharging
        vehicleReadings.socRange += self.batteryStatus
        # self.inactivityTimer = threading.Timer(5.0, self.poweroff)
        self.inactivityTimer = RepeatableTimer(10.0, self.poweroff)
    def updateStandState(self, state):
        self.standState = state
        self.standMonitor(state)
    
    def poweroff(self):
        print('User inactive.')
        vehicleEvents.onUserInactivity(0)

    def standMonitor(self, state):
        if(state == 1):
            self.inactivityTimer.start()
        elif (state == 0):
            self.inactivityTimer.cancel()

    def uiMonitor(self, state):
        if(self.standState == 1 and state == 1):
            self.inactivityTimer.cancel()
            self.inactivityTimer.start()

    def onBikeOff(self):
        subprocess.call('vcgencmd display_power 0', shell=True)
        print('X Started.')
        print('Bike is Off.')

    def onBikeOn(self):
        subprocess.call('vcgencmd display_power 1', shell=True)
        print('Chromium Killed')
        print('Bike is On.')

    def batteryStatus(self, soc, rangeSuste, rangeThikka, rangeBabbal):
        self.stateOfCharge = soc

    def onCharging(self, state):
        if(state == True):
            self.socOnChargeStart = self.stateOfCharge
            self.socOnChargeStartTime = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        else:
            self.socOnChargeEnd = self.stateOfCharge
            self.socOnChargeEndTime = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            if(self.socOnChargeStart == None):
                return

            deltaSOC = self.socOnChargeEnd - self.socOnChargeStart
            if(deltaSOC > 1.0):
                costOfCharging = round(deltaSOC * COST_FACTOR, 2)
                dataToBeSaved = [self.socOnChargeStart, self.socOnChargeEnd, self.socOnChargeStartTime, self.socOnChargeEndTime, costOfCharging]
                self.addToList(dataToBeSaved)
                with open(CHARGE_SAVINGS_FILE, 'w') as f:  # writing JSON object
                    json.dump(self.chargeSavingsData, f)
            else:
                print('Delta SOC is less than 1%.')

    def addToList(self, data):
        if(len(self.chargeSavingsData) > MAX_DATA_COUNT):
            del self.chargeSavingsData[0]
        self.chargeSavingsData.append(data)
