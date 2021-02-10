import serial
import time
from event_handler import *
from gps import *
import requests
from bike_credentials import *

MAX_COUNT = 8
AT_COMMAND_PORT = "/dev/ttyUSB2"
GPS_DATA_PORT = "/dev/ttyUSB1"

class Quectel():
    __instance__ = None
    atCommandPort = None

    def __init__(self):
        """ Constructor.
        """
        self.gpsMgr = None
        self.isLowBalanceNotified = False
        self.isCriticalLowBalanceNotified = False
        self.phoneNumber = None
        if Quectel.__instance__ is None:
            self.initializeConnection()
            if Quectel.atCommandPort:
                Quectel.__instance__ = self
                self.subscribeToEvents()
                self.enableGPS()
            else:
                return None
        else:
            raise Exception("You cannot create another Quectel object")

    @staticmethod
    def getInstance():
        """ Static method to fetch the current instance.
        """
        if not Quectel.__instance__:
            Quectel()
        elif not Quectel.atCommandPort:
            self.initializeConnection()
        return Quectel.__instance__
    
    def initializeConnection(self):
        if not Quectel.atCommandPort:
            try:
                Quectel.atCommandPort = serial.Serial(AT_COMMAND_PORT, baudrate = 115200, timeout = 1)
            except (FileNotFoundError, serial.serialutil.SerialException) as error:
                print(error)
                return
    def subscribeToEvents(self):
        vehicleEvents.guiReady += self.onGUIReady
        vehicleEvents.refreshSettingsData += self.onGUIReady

    def unsubscribeToEvents(self):
        vehicleEvents.guiReady -= self.onGUIReady
        vehicleEvents.refreshSettingsData -= self.onGUIReady

    def __del__(self):
        if Quectel.atCommandPort != None:
            Quectel.atCommandPort.close()
        self.unsubscribeToEvents()
        print("Destroyed Quectel Object.")

    def send(self, cmd):
        try:
            while(Quectel.atCommandPort.in_waiting > 0):
                # Read data out of the buffer until a carraige return / new line is found
                serialString = Quectel.atCommandPort.readline()
                # Print the contents of the serial data
                print(serialString.decode('Ascii'))
            Quectel.atCommandPort.write(str.encode(cmd + '\r'))
        except (OSError) as error:
            print(error)

    def getWriteResponse(self):
        Quectel.atCommandPort.readline()
        Quectel.atCommandPort.flush()
        responseEncoded = Quectel.atCommandPort.readline()
        return responseEncoded.decode()

    def getInfo(self, name):
        count = 0
        match = name + ':'
        while(count < MAX_COUNT):
            responseEncoded = Quectel.atCommandPort.readline()
            response = responseEncoded.decode()
            # print(response)
            if(match in response):
                return response
            else:
                count=count + 1
    
    def test(self):
        cmd = "AT"
        self.send(cmd)
        response  = self.getWriteResponse()
        print("AT response: ",response)

    def enableGPS(self):
        cmd = "AT+QGPS=1"
        self.send(cmd)
        response  = self.getWriteResponse()
        print('Enable GPS Response: ', response)
        self.gpsMgr = GPS.getInstance(self)
        print('GPS : ', self.gpsMgr)
        # if(self.gpsMgr != None):
        #     vehicleReadings.network({'gpsStatus': True})
    
    def disableGPS(self):
        cmd = "AT+QGPSEND"
        self.send(cmd)
        response  = self.getWriteResponse()
        print('Disable GPS Response: ', response)
        self.gpsMgr.stopGPS()
        del self.gpsMgr
        self.gpsMgr = None
        vehicleReadings.network({'gpsStatus': False})
    
    def getSimStat(self):
        cmd = "AT+QSIMSTAT?"
        name = "QSIMSTAT"
        self.send(cmd)
        Quectel.atCommandPort.readline()
        response = self.getInfo(name)
        print(response)
        insertionStatusReport = response[11]
        insertedStatus = response[13]
        return (insertionStatusReport, insertedStatus)
    
    def getNetworkInfo(self):
        cmd = "AT+QSPN"
        name = "QSPN"
        self.send(cmd)
        response = self.getInfo(name)
        print(response)
        nameSplit = response.split(':')
        infoSplit = nameSplit[1].split(',')
        networkName = infoSplit[1].strip('"')
        return networkName
    
    def getSimInfo(self):
        simStat = self.getSimStat()
        networkName =""
        if(simStat[1] == '1'):
            networkName = self.getNetworkInfo()
        return (simStat[1], networkName)

    def getBalance(self):
        name = 'CUSD'
        cmd = 'AT+CSCS="GSM"'
        self.send(cmd)
        response = self.getWriteResponse()
        print(response)
        time.sleep(1)
        cmd = 'AT+QURCCFG="urcport","usbat"'
        self.send(cmd)
        response = self.getWriteResponse()
        print('QURCCFQ write: ', response)
        time.sleep(1)
        cmd = 'AT+CUSD=1,"*101#",15'
        self.send(cmd)
        response = self.getWriteResponse()
        print('CUSD write: ', response)

        Quectel.atCommandPort.readline()
        response = self.getInfo(name)
        balance = None
        print('CUSD response: ', response)
        # if(response != None):
        #     nameSplit = response.split(':')
        #     balance = nameSplit[2].strip().strip('.')
        #     print('Extracted Balance: ', balance)
        if(response != None):
            title = 'Balance:'
            titleIndex = response.find(title)
            # print('Extracted title index: ', titleIndex)
            if(titleIndex != -1):
                nameSplit = response.split(':')
                balance = nameSplit[2].strip().strip('.')
                print('Extracted Balance: ', balance)
        return balance

    def getPhoneNumber(self):
        name = 'CUSD'
        cmd = 'AT+CSCS="GSM"'
        self.send(cmd)
        response = self.getWriteResponse()
        print(response)
        time.sleep(1)
        cmd = 'AT+QURCCFG="urcport","usbat"'
        self.send(cmd)
        response = self.getWriteResponse()
        print('QURCCFQ write: ', response)
        time.sleep(1)
        cmd = 'AT+CUSD=1,"*103#",15'
        self.send(cmd)
        response = self.getWriteResponse()
        print('CUSD write: ', response)

        Quectel.atCommandPort.readline()
        response = self.getInfo(name)
        number = None
        print('CUSD response: ', response)
        if(response != None):
            title = 'Your number is '
            titleIndex = response.find(title)
            if(titleIndex != -1):
                # print('Extracted Index: ', titleIndex + len(title))
                numberIndex = titleIndex+len(title)
                number = response[numberIndex:numberIndex+10]
                self.phoneNumber = number
                print('Extracted phone number: ', number)
        return number

    def onGUIReady(self):
        [simStatus, networkName] = self.getSimInfo()
        vehicleReadings.network({'simStatus': simStatus, 'networkName': networkName})
        balance = self.getBalance()
        if balance != None:
            vehicleReadings.network({'balance': balance})
        
        if(self.phoneNumber == None):
            self.getPhoneNumber()
        if(self.phoneNumber != None):
            vehicleReadings.network({'number': self.phoneNumber})
    
    def checkForLowBalance(self, balance):
        if balance != None:
            title = "Rs. "
            titleIndex = balance.find(title)
            if(titleIndex != -1):
                nameSplit = balance.split('. ')
                print(nameSplit)
                balanceNum = nameSplit[1].strip()
                if((float(balanceNum) - 25.0) < 0):
                    print('Balance Low.')
                    self.sendBalanceInformation(balance, 0)
                else:
                    print('Balance is fine.')
    
    def sendBalanceInformation(self, balance, data):
        url = "http://yatri-embedded-env.eba-gpw9ppqj.ap-south-1.elasticbeanstalk.com/api/v1/bikes/low-balance"
        payload = '{\r\n    \"balance\": \"'+ str(balance) + '\",\r\n    \"data\": \"' + str(data) + '\"\r\n}'
        print(payload)
        response = requests.request("POST", url, headers=headerLowBalance, data=payload)
        print(response.status_code)

        # if self.gpsMgr != None:
        #     vehicleReadings.network({'gpsStatus': True})
        # else:
        #     vehicleReadings.network({'gpsStatus': False})
if __name__ == "__main__":
    quectel = Quectel()
    quectel.test()
    # quectel.disableGPS()
    simStat = quectel.getSimStat()
    print(simStat)
    if(simStat[1] == '1'):
        networkName = quectel.getNetworkInfo()
        print(networkName)
    time.sleep(2)
    balance = quectel.getBalance()
    quectel.checkForLowBalance(balance)
    time.sleep(2)
    print('Getting Phone Number.')
    quectel.getPhoneNumber()
