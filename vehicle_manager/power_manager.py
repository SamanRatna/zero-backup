from event_handler import *
import threading
from gpio_manager import RepeatableTimer
import subprocess
import json
from datetime import datetime
import requests
from bike_credentials import *

COST_FACTOR = 1.2
CHARGE_SAVINGS_FILE = 'charge-savings.json'
MAX_DATA_COUNT = 30

class PowerManager():
    def __init__(self):
        self.standState = 0
        self.chargeCycle = 0
        self.isCharging = False
        self.lastChargeUpdate = None
        self.socOnChargeStart = None
        self.socOnChargeEnd = None
        self.chargeSavingsData = []
        try:
            with open(CHARGE_SAVINGS_FILE, 'r') as f:
                self.chargeSavingsData = json.load(f)
                self.chargeCycle = self.chargeSavingsData[-1][0]

        except (OSError, json.decoder.JSONDecodeError) as error:
            print(error)

        vehicleEvents.onStandSwitch += self.updateStandState
        vehicleEvents.onUserInteraction += self.uiMonitor
        vehicleEvents.bikeOff += self.onBikeOff
        vehicleEvents.bikeOn += self.onBikeOn
        vehicleEvents.charging += self.onCharging
        vehicleReadings.socRange += self.batteryStatus
        # vehicleEvents.bluetoothStatus += self.onBluetoothStatusChange
        vehicleEvents.onChargeCostsRequest += self.onChargeCostsRequest
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

    def batteryStatus(self, soc, soh, rangeSuste, rangeThikka, rangeBabbal):
        self.stateOfCharge = soc
        if(self.isCharging):
            if(self.stateOfCharge - self.lastChargeUpdate >= 5):
                self.sendStateOfCharge(int(self.stateOfCharge), self.isCharging)

    def onCharging(self, state):
        self.isCharging = state
        if(state == True):
            self.socOnChargeStart = self.stateOfCharge
            self.socOnChargeStartTime = int(datetime.now().timestamp())
            if(self.lastChargeUpdate == None):
                self.sendStateOfCharge(int(self.stateOfCharge), self.isCharging)
        else:
            if(self.lastChargeUpdate != None):
                self.sendStateOfCharge(int(self.stateOfCharge), self.isCharging)
            self.socOnChargeEnd = self.stateOfCharge
            self.socOnChargeEndTime = int(datetime.now().timestamp())
            if(self.socOnChargeStart == None):
                return

            deltaSOC = self.socOnChargeEnd - self.socOnChargeStart
            if(deltaSOC > 1.0):
                costOfCharging = round(deltaSOC * COST_FACTOR, 2)
                self.chargeCycle += 1
                dataToBeSaved = [self.chargeCycle, self.socOnChargeStart, self.socOnChargeEnd, self.socOnChargeStartTime, self.socOnChargeEndTime, costOfCharging]
                self.addToList(dataToBeSaved)
                with open(CHARGE_SAVINGS_FILE, 'w') as f:  # writing JSON object
                    json.dump(self.chargeSavingsData, f)
                vehicleReadings.chargeCostsForBluetooth(self.chargeSavingsData)
            else:
                print('Delta SOC is less than 1%.')

    def addToList(self, data):
        if(len(self.chargeSavingsData) > MAX_DATA_COUNT):
            del self.chargeSavingsData[0]
        self.chargeSavingsData.append(data)

    # def onBluetoothStatusChange(self, state):
    #     print('Bluetooth Status Changed.')
    #     if(state == 'SERVICES_READY'):
    #         vehicleReadings.chargeCostsForBluetooth(self.chargeSavingsData)
    
    def searchForCycle(self, cycle):
        # print('Last data: ', int(self.chargeSavingsData[-1][0]))
        if(cycle > int(self.chargeSavingsData[-1][0])):
            return None
        index = 0
        for data in self.chargeSavingsData:
            print(int(data[0]))
            if(cycle < int(data[0])):
                break
            else:
                cycle += 1
                index += 1
        return index

    def onChargeCostsRequest(self, cycle):
        print('ChargeCosts: Cycle Received from Bluetooth: ', cycle)
        index = self.searchForCycle(cycle)
        print('Latest Charge Cycle Index: ', index)
        if(index != None):
            vehicleReadings.chargeCostsForBluetooth(self.chargeSavingsData[index:])

    def sendStateOfCharge(self, soc, chargingStatus):
        current_soc = str(soc)
        current_status = str(chargingStatus).lower()
        print(current_soc, current_status )
        url = "http://yatri-embedded-env.eba-gpw9ppqj.ap-south-1.elasticbeanstalk.com/api/v1/bikes/batteries/" + battery_id
        payload = '{\r\n    \"soc\": '+ current_soc + ',\r\n    \"isCharging\": ' + current_status + '\r\n}'
        response = requests.request("PATCH", url, headers=headers, data=payload)
        print(response.text)
        if(chargingStatus == True):
            self.lastChargeUpdate = soc
        else:
            self.lastChargeUpdate = False
