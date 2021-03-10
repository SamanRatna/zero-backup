from event_handler import *
import requests
from datetime import datetime
from bike_credentials import *
from url import *
from multiprocessing import Process, Queue
import time

TIMEOUT = 7

class Telematics():
    def __init__(self):
        self.chargeCycle = 0
        self.isCharging = False
        self.isFastCharging = False
        self.lastChargeUpdate = None
        self.stateOfCharge = None
        self.socOnChargeStart = None
        self.socOnChargeEnd = None
        self.chargeUpdateQueue = Queue()
        self.chargeUpdatedQueue = Queue()
        self.worker = None
        vehicleEvents.charging += self.onCharging
        # vehicleReadings.batteryStatus += self.batteryStatus
        vehicleReadings.socRange += self.batteryStatus
    
    def onCharging(self, isCharging, isFastCharging):
        print('TELEMATICS :: Charging = ', isCharging)
        self.isCharging = isCharging
        self.isFastCharging = isFastCharging
        self.getLastChargeUpdate()
        if(isCharging == True):
            if(self.stateOfCharge == None):
                return
            
            self.socOnChargeStart = self.stateOfCharge
            self.socOnChargeStartTime = int(datetime.now().timestamp())
            if(self.lastChargeUpdate == None or self.lastChargeUpdate == False):
                self.sendStateOfCharge(int(self.stateOfCharge), self.isCharging, self.isFastCharging)
        else:
            if(self.lastChargeUpdate != None and self.lastChargeUpdate != False):
                self.sendStateOfCharge(int(self.stateOfCharge), self.isCharging, self.isFastCharging)
            elif(self.worker != None):
                if(self.worker.is_alive()):
                    self.sendStateOfCharge(int(self.stateOfCharge), self.isCharging, self.isFastCharging)
            self.socOnChargeEnd = self.stateOfCharge
            self.socOnChargeEndTime = int(datetime.now().timestamp())
            if(self.socOnChargeStart == None):
                return
    
    def getLastChargeUpdate(self):
        print('Charge Update Queue Emtpy: ', self.chargeUpdatedQueue.empty())
        while not self.chargeUpdatedQueue.empty():
            self.lastChargeUpdate = self.chargeUpdatedQueue.get()[1]
        print('El Psy Congroo : lastChargeUpdate: ', self.lastChargeUpdate)

    def batteryStatus(self, soc, soh, rangeSuste, rangeThikka, rangeBabbal):
        print('TELEMATICS :: State of Charge = ', soc)
        print('TELEMATICS :: Charging Status = ', self.isCharging)
        self.stateOfCharge = soc
        if(self.isCharging):
            print('TELEMATICS :: Sending the data.')
            self.getLastChargeUpdate()
            if(self.lastChargeUpdate == None or self.lastChargeUpdate == False):
                self.sendStateOfCharge(int(self.stateOfCharge), self.isCharging, self.isFastCharging)
            elif(self.stateOfCharge - self.lastChargeUpdate >= 2):
                self.sendStateOfCharge(int(self.stateOfCharge), self.isCharging, self.isFastCharging)
    
    def sendStateOfCharge(self, soc, chargingStatus, isFastCharging):
        self.chargeUpdateQueue.put([soc, chargingStatus, isFastCharging])
        if(self.worker == None):
            self.worker = Process(target=self.updateStateOfCharge, args=(self.chargeUpdateQueue, self.chargeUpdatedQueue,))
            self.worker.start()
        elif(not self.worker.is_alive()):
            self.worker = Process(target=self.updateStateOfCharge, args=(self.chargeUpdateQueue, self.chargeUpdatedQueue,))
            self.worker.start()
            print('Starting worker.')
        else:
            print('Worker is alive.')

    def updateStateOfCharge(self, chargeUpdateQueue, chargeUpdatedQueue):
        if(chargeUpdateQueue.empty()):
            print('Nothing to be pushed to server.')
            return()
        lastChargeUpdate = None
        lastChargeUpdateType = None
        while not chargeUpdateQueue.empty():
            data = chargeUpdateQueue.get()
            soc = data[0]
            chargingStatus = data[1]
            fastChargingStatus = data[2]
            if(lastChargeUpdate != None):
                if(chargingStatus == lastChargeUpdateType):
                    if(abs(soc - lastChargeUpdate) < 2):
                        continue
            print('Send State of Charge: ', soc, chargingStatus)
            current_soc = str(soc)
            current_status = str(chargingStatus).lower()
            current_eta = str(int((100 - soc)*180/100))
            current_eta = current_eta + ' mins'
            try:
                print('Trying to reach the server.')
                url = URL_SOC_UPDATE + batteryId

                payload = None
                if(chargingStatus):
                    payload = '{\r\n    \"soc\": '+ current_soc + ',\r\n    \"isCharging\": ' + current_status + ',\r\n  \"eta\":' +'\"' +current_eta + '\"'+'\r\n}'
                else:
                    payload = '{\r\n    \"soc\": '+ current_soc + ',\r\n    \"isCharging\": ' + current_status + '\r\n}'
                print(payload)
                response = requests.request("PATCH", url, headers=headerCharge, data=payload, timeout=TIMEOUT)
                print(response.text)
                # print(response.status_code)
                if(response.status_code == 200):
                    if(chargingStatus == False):
                        soc = None
                    lastChargeUpdate = soc
                    lastChargeUpdateType = chargingStatus
                    print('Server responded success.')
                    chargeUpdatedQueue.put([chargingStatus, soc])
            except Exception as err:
                print('TELEMATICS :: Exception while trying to reach the server.')
                print(err)

if __name__=="__main__":
    tele = Telematics()