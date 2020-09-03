import serial
from event_handler import *
import threading
import time
import math
from quectel import *
GPS_DATA_PORT = "/dev/ttyUSB1"


class GPS():
    # _counter = 0
    def __init__(self, _gpsHandle):
        # GPS._counter = GPS._counter + 1
        # print('GPS Counter: ', GPS._counter)
        # print('GPS Constructor: GPS Object Id: ', self)
        self.gpsHandle = _gpsHandle
        self.gpsPort = None
        self.gpsHistory = []
        if(self.gpsHandle == None):
            return

        print("Receiving GPS data")
        self.gpsPort = serial.Serial(GPS_DATA_PORT, baudrate = 115200, timeout = 0.5)
        self.stopGPSThread = False
        self.tGPS = threading.Thread(target = self.startGPS)
        self.tGPS.start()
    
    def __del__(self):
        # GPS._counter = GPS._counter - 1
        if(self.gpsPort):
            self.gpsPort.close()
        print("Destroyed GPS Object.")

    def parseGPS(self, data):
        decodedData = data.decode()
        # print(decodedData)

        if decodedData[1:6] == "GPRMC":
            sdata = decodedData.split(",")
            # print(sdata)
            if sdata[2] == 'V':
                print("no satellite data available")
                return
            # print("-----Parsing GPRMC-----")
            # print(sdata)
            gmttime = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
            # lat = decode(sdata[3]) #latitude
            lat = round(float(sdata[3])/100, 4)
            dirLat = sdata[4]      #latitude direction N/S
            # lon = decode(sdata[5]) #longitute
            lon = round(float(sdata[5])/100, 4)
            dirLon = sdata[6]      #longitude direction E/W
            speed = sdata[7]       #Speed in knots
            trCourse = sdata[8]    #True course
            date = sdata[9][0:2] + "/" + sdata[9][2:4] + "/" + sdata[9][4:6]
                               #date
            variation = sdata[10]  #variation
            degreeChecksum = sdata[12]
            # print('Degree Checksum: '+degreeChecksum)
            dc = degreeChecksum.split("*")
            degree = dc[0]        #degree
            checksum = dc[1]      #checksum
            # print("time : %s, latitude : %s(%s), longitude : %s(%s), speed : %s, True Course : %s, Date : %s, Magnetic Variation : %s(%s),Checksum : %s "%    (time,lat,dirLat,lon,dirLon,speed,trCourse,date,variation,degree,checksum))
            # print("Latitude : ", lat)
            # print("Longitude: ", lon)
            self.gpsHistory.append([lat,lon])
            vehicleReadings.gpsLocation(lat, lon)
            time.sleep(2.0)
        # else:
        #     print("Printed data is ",data[0:6])

    def decode(self, coord):
        #Converts DDDMM.MMMMM -> DD deg MM.MMMMM min
        x = coord.split(".")
        head = x[0]
        tail = x[1]
        deg = head[0:-2]
        min = head[-2:]
        return deg + " deg " + min + "." + tail + " min"

    def startGPS(self):
        self.stopGPSThread = False
        while not self.stopGPSThread:
           data = self.gpsPort.readline()
           self.parseGPS(data)

    def stopGPS(self):
        self.stopGPSThread = True
    def calculateHeading(self, location_a, location_b):
        if (len(self.gpsHistory) < 3):
            return
        lat_a = self.gpsHistory[len(self.gpsHistory) - 1][0]
        lat_b = self.gpsHistory[len(self.gpsHistory)][0]
        lon_a = self.gpsHistory[len(self.gpsHistory) - 1][1]
        lon_b = self.gpsHistory[len(self.gpsHistory)][0]

        delta_lon = lon_b - lon_a
        
        x = math.cos(lat_b) * math.sin(delta_lon)
        y = math.cos(lat_a) * math.sin(lat_b) - math.sin(lat_a)*math.cos(lat_b)*math.cos(delta_lon)
        heading = math.atan2(x,y)
        print('Heading: ', heading)

if __name__ == "__main__":
    quectel = Quectel.getInstance()
    gpsMgr = GPS(quectel)
    