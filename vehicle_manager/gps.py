# from time import sleep
import serial
from event_handler import *
import threading
import time

portwrite = "/dev/ttyUSB2"
port = "/dev/ttyUSB1"
 
# print("Connecting port")
# serw = serial.Serial(portwrite, baudrate = 115200, timeout = 1)
# serw.write(str.encode('AT+QGPS=1\r'))
# serw.close()
# time.sleep(0.5)
 
# print("Receiving GPS data")
# ser = serial.Serial(port, baudrate = 115200, timeout = 0.5)


class GPS():
    def __init__(self):
        print("Connecting port")
        self.serw = serial.Serial(portwrite, baudrate = 115200, timeout = 1)
        self.serw.write(str.encode('AT+QGPS=1\r'))
        self.serw.close()
        time.sleep(0.5)

        print("Receiving GPS data")
        self.ser = serial.Serial(port, baudrate = 115200, timeout = 0.5)
        self.tGPS = threading.Thread(target = self.startGPS)
        self.tGPS.start()
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
            vehicleReadings.gpsLocation(lat, lon)
            time.sleep(5.0)
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
        while True:
           data = self.ser.readline()
           self.parseGPS(data)