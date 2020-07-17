import serial

MAX_COUNT = 4
AT_COMMAND_PORT = "/dev/ttyUSB2"
GPS_DATA_PORT = "/dev/ttyUSB1"

class Quectel():
    __instance__ = None

    def __init__(self):
        """ Constructor.
        """
        if Quectel.__instance__ is None:
            Quectel.__instance__ = self
            self.atCommandPort = serial.Serial(AT_COMMAND_PORT, baudrate = 115200, timeout = 1)
        else:
            raise Exception("You cannot create another Quectel object")

    @staticmethod
    def getInstance():
        """ Static method to fetch the current instance.
        """
        if not Quectel.__instance__:
            Quectel()
        return Quectel.__instance__

    def __del__(self):
        self.atCommandPort.close()
        print("Destroyed Quectel Object.")

    def send(self, cmd):
        self.atCommandPort.write(str.encode(cmd + '\r'))

    def getWriteResponse(self):
        self.atCommandPort.readline()
        self.atCommandPort.flush()
        responseEncoded = self.atCommandPort.readline()
        return responseEncoded.decode()

    def getInfo(self, name):
        count = 0
        match = name + ':'
        while(count < MAX_COUNT):
            responseEncoded = self.atCommandPort.readline()
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
        print(response)

    def enableGPS(self):
        cmd = "AT+QGPS=1"
        self.send(cmd)
        response  = self.getWriteResponse()
        print(response)
    
    def disableGPS(self):
        cmd = "AT+QGPSEND"
        self.send(cmd)
        response  = self.getWriteResponse()
        print(response)
    
    def getSimStat(self):
        cmd = "AT+QSIMSTAT?"
        name = "QSIMSTAT"
        self.send(cmd)
        self.atCommandPort.readline()
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
        return (simState[1], networkName)

if __name__ == "__main__":
    quectel = Quectel()
    quectel.test()
    quectel.disableGPS()
    simStat = quectel.getSimStat()
    print(simStat)
    if(simStat[1] == '1'):
        networkName = quectel.getNetworkInfo()
        print(networkName)