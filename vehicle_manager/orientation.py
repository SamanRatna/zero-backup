# Simple Adafruit BNO055 sensor reading example.  Will print the orientation
# and calibration data every second.
#
# Copyright (c) 2015 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import logging
import sys
import time
from event_handler import *

from Adafruit_BNO055 import BNO055
ORIENTATION_DATA_PORT = '/dev/serial0'
RESET_PIN = 18

class Orientation():
    # _counter = 0
    __instance__ = None
    dataPort = None
    @staticmethod
    def getInstance():
        """ Static method to fetch the current instance.
        """
        if not Orientation.__instance__:
            Orientation.__instance__ = Orientation()
        elif not Orientation.dataPort:
            self.initializeConnection()
        print('Returning Orientation instance: ', Orientation.__instance__)
        return Orientation.__instance__

    def initializeConnection(self):
        if not Orientation.dataPort:
            try:
                Orientation.dataPort = BNO055.BNO055(serial_port=ORIENTATION_DATA_PORT, rst=RESET_PIN)

                # Initialize the BNO055 and stop if something went wrong.
                if not Orientation.dataPort.begin():
                    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')
                
                # Print system status and self test result.
                status, self_test, error = Orientation.dataPort.get_system_status()
                print('System status: {0}'.format(status))
                print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
                # Print out an error if system status is in error mode.
                if status == 0x01:
                    print('System error: {0}'.format(error))
                    print('See datasheet section 4.3.59 for the meaning.')

                # Print BNO055 software revision and other diagnostic data.
                sw, bl, accel, mag, gyro = Orientation.dataPort.get_revision()
                print('Software version:   {0}'.format(sw))
                print('Bootloader version: {0}'.format(bl))
                print('Accelerometer ID:   0x{0:02X}'.format(accel))
                print('Magnetometer ID:    0x{0:02X}'.format(mag))
                print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))
            except Exception as error:
                print(error)
                return

    def __init__(self):
        # GPS._counter = GPS._counter + 1
        # print('GPS Counter: ', GPS._counter)
        # print('GPS Constructor: GPS Object Id: ', self)
        self.initializeConnection()
        self.tOrientation = None
        self.navigationMode = False
        vehicleEvents.onNavigation += self.onNavigation
        # self.onNavigationStart()
    def __del__(self):
        # GPS._counter = GPS._counter - 1
        vehicleEvents.onNavigation -= self.onNavigation
        print("Destroyed Orientation Object.")
    
    def onNavigationStart(self):
        while self.navigationMode:
            # Read the Euler angles for heading, roll, pitch (all in degrees).
            heading, roll, pitch = Orientation.dataPort.read_euler()
            # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
            sys, gyro, accel, mag = Orientation.dataPort.get_calibration_status()
            # Print everything out.
            print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\tSys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(
                  heading, roll, pitch, sys, gyro, accel, mag))
            heading = round(heading, 2)
            roll = round(roll, 2)
            pitch = round(pitch, 2)
            vehicleReadings.orientation(heading, roll, pitch)
            time.sleep(1)

    def onNavigation(self,request):
        print('Orientation: Navigation Request: ',request)
        if(request):
            self.navigationMode = True
            # self.onNavigationStart()
            if(self.tOrientation and self.tOrientation.is_alive()):
                print(self, ': Orientation Thread already active.')
                return
            print(self, ': About to start Orientation Thread')
            self.tOrientation = threading.Thread(target = self.onNavigationStart)
            self.tOrientation.start()
        else:
            print(self, ': About to stop Orientation Thread')
            self.navigationMode = False

if __name__ == "__main__":
    orientation = Orientation.getInstance()
