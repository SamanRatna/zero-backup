import logging
import threading
import time
import can
import random
import os
from event_handler import *
from watchdog import Watchdog
import subprocess
import math

RPM_TO_KMPH = 0.025
ODO_FACTOR = 0.1
TRACTION_MIN_FACTOR = 0.25
SOC_FACTOR = 0.01
SOH_FACTOR = 0.01
TMP_FACTOR = 0.1

RANGE_ON_FULL_AH = 180
AH_ON_FULL_SOH = 90

class CANHandler:
    def __init__(self):
        # subprocess.call('sudo ifconfig can0 up', shell=True)

        #Parameters
        self.iterator               = 0
        self.isCharging             = False
        self.isFastCharging         = False
        self.chargingCurrent        = 0     # Ampere
        self.chargingCurrentCharger = 0     # Ampere
        self.packVoltage            = 0     # Volts
        self.stateOfCharge          = 0     # Percentage
        self.stateOfHealth          = 0     # Percentage
        self.timeToCharge           = 0     # Minutes
        self.timeToDischarge        = 0     # Minutes
        self.highTemp               = 0     # Celsius      
        self.lowTemp                = 0     # Celsius
        self.bikeSpeed              = 0     # kmph
        self.maxTorque              = 0     # Newton-meter
        self.actualTorque           = 0     # Newton-meter
        self.batteryTemperature     = 0     # Celsius
        self.vcuTemperature         = 0
        self.motorTemp              = 0     # Celsius
        self.driveMode              = 0
        self.odometer               = 0     # km
        self.peakChargingCurrent    = 0     # Ampere
        self.peakDischargingCurrent = 0     # Ampere
        self.dischargingCurrent     = 0     # Ampere
        self.power                  = 0     # W
        self.remainingCapacity      = 0     # Ampere-hour
        self.rangeThikka            = 0     # km
        self.rangeSuste             = 0     # km
        self.rangeBabbal            = 0     # km
        self.controllerTemperature  = 0
        self.motorCurrent           = 0
        self.motorVoltage           = 0

        #Configure CAN Interface
        can.rc['interface'] = 'socketcan_native'
        can.rc['channel'] = 'can0'
        self.bus = can.interface.Bus()    

        # self.watchdog = Watchdog(30, self.watchdogHandler)

        #Start CAN
        vehicleEvents.guiReady += self.onGUIReady
        vehicleEvents.autoOff += self.onAutoOff
        self.startCAN()
        vehicleEvents.bluetoothStatus += self.onBluetoothStatusChange

    def setChargingStatus(self, status):
        if(status != self.chargingStatus):
            print('Charge Status: ', status)
            self.chargingStatus = status
            vehicleEvents.onCharging(self.chargingStatus)

    def onBluetoothStatusChange(self, state):
        # print('BLE is ready.')
        if(state == 'SERVICES_READY'):
            vehicleReadings.batteryStatus(self.stateOfCharge)

    def watchdogHandler(self):
        print('Something has gone wrong!!!')
        subprocess.call('sudo ifconfig can0 down', shell=True)
        time.sleep(3.0)
        subprocess.call('sudo ifconfig can0 up', shell=True)
        time.sleep(3.0)
        subprocess.call('sudo systemctl restart vmgr.service', shell=True)


    def extractCANData(self):
        while True:
            message = self.bus.recv(0.1)
            if message is not None:
                if message.arbitration_id != 128:
                    # Motor Controller
                    if message.arbitration_id == 0x124:
                        data = message.data
                        speed = round((((data[1])*256 + (data[0]))* RPM_TO_KMPH), 2)
                        # Fix negative velocity issue
                        if speed > 240:
                            self.bikeSpeed = 0
                        else:
                            self.bikeSpeed = speed
                        vehicleReadings.speedReading(self.bikeSpeed)


                    if message.arbitration_id == 0x125:
                        data = message.data
                        odometer = round((data[3] * 16777216 + data[2] * 65536  + data[1] * 256 + data[0])*ODO_FACTOR, 2)
                        tractionHour = round((data[5] * 256 + data[4] + data[6]*TRACTION_MIN_FACTOR/60), 2)

                        self.odometer = odometer
                        vehicleReadings.odoReading(self.odometer)
                        vehicleReadings.distancehour(self.odometer, tractionHour)
                    if message.arbitration_id == 0x126:
                        data = message.data
                        tripDistance = round((data[3] * 16777216 + data[2] * 65536  + data[1] * 256 + data[0])*ODO_FACTOR, 2)

                        motorTemperature = int((data[5]*256 + data[4]))
                        controllerTemperature = int(data[6])
                        vehicleReadings.motorTemperature(motorTemperature, controllerTemperature)

                    #ION BMS
                    if message.arbitration_id == 0x18FF05D0:
                        data = message.data
                        soc = round((data[0] * 256 + data[1])*SOC_FACTOR, 2)
                        soh = round((data[2] * 256 + data[3])*SOH_FACTOR, 2)

                        if(abs(soc - self.stateOfCharge) > 0.01):
                            self.stateOfCharge = soc
                            self.stateOfHealth = soh
                            vehicleReadings.batteryStatus(self.stateOfCharge)
                            #caculate range
                            # ah = soc * AH_ON_FULL_SOH * soh / 10000
                            # print('Ah: ', ah)
                            # estimatedRange = round(RANGE_ON_FULL_AH * (self.stateOfCharge * AH_ON_FULL_SOH * soh / (100*100)) / AH_ON_FULL_SOH, 1)
                            estimatedRange = round(RANGE_ON_FULL_AH * (soc * soh / (100*100)), 1)
                            self.rangeSuste = estimatedRange
                            vehicleReadings.socRange(soc, soh, estimatedRange, estimatedRange, estimatedRange)

                        self.stateOfCharge = soc

                    if message.arbitration_id == 0x18FF03D0:
                        data = message.data
                        batteryTemperature = round((data[4] * 256 + data[5])*TMP_FACTOR, 1)
                        if(batteryTemperature - self.batteryTemperature > 0.1):
                            self.batteryTemperature = batteryTemperature
                            vehicleReadings.batteryTemperature(self.batteryTemperature)
                    # if message.arbitration_id == 0x18FF07D0:
                    #     data = message.data
                    #     isCharging = data[0] * 0x20
                    #     isDischarging = data[0] * 0x40
                    #     print('Charging Status: ', isCharging)
                    #     print('Discharging Status: ', isDischarging)

                    # Elcon Charger
                    if message.arbitration_id == 0x18FF50E5:
                        data = message.data
                        current = round((data[2]*256 + data[3])*0.1, 2)
                        # print('Charging Current: ', current, 'A')
                        isCharging = None
                        # isFastCharging = None
                        if(current > 0.1):
                            isCharging = True
                            # isFastCharging = False
                            # print('Charging')
                        else:
                            isCharging = False
                            # isFastCharging = False

                        if(isCharging != self.isCharging):
                            self.isCharging = isCharging
                            # self.isFastCharging = isFastCharging
                            vehicleEvents.charging(self.isCharging, False)
                    # VCU
                    if message.arbitration_id == 0x1E00103:
                        data=message.data
                        if(data[0] == 0x6):
                            if(data[1] == 0x1):
                                # ignition off
                                print('Turning bike off')
                                # vehicleEvents.bikeOff()
                                vehicleEvents.bikeOnOff(False)
                            elif(data[1] == 0x2):
                                # ignition on
                                print('Turning bike on')
                                # vehicleEvents.bikeOn()
                                vehicleEvents.bikeOnOff(True)
                            elif(data[1] == 0x5):
                                vehicleEvents.vcuCharging(False)
                        
                        if(data[0] == 0x1):
                            vehicleEvents.onSideLight(data[1])
                            vehicleEvents.onButtonPress()
                            # if(data[1] == 0x1):
                            #     # no side lights
                            # elif(data[2] == 0x2):
                            #     # left side light
                            # elif(data[3] == 0x3):
                            #     # right side light
                            # elif(data[4] == 0x4):
                            #     # both side lights
                        
                        elif(data[0] == 0x2): # low beam
                            vehicleEvents.onHeadLight(1, data[1])
                            vehicleEvents.onButtonPress()
                        elif(data[0] == 0x3): # high beam
                            vehicleEvents.onHeadLight(2, data[1])
                            vehicleEvents.onButtonPress()

                        
                        elif(data[0] == 0x4):
                            vehicleReadings.bikeMode(data[1])
                            vehicleEvents.onButtonPress()
                            # if(data[1] == 0x1):
                            #     # reverse mode
                            # elif(data[1] == 0x2):
                            #     # standby mode
                            # elif(data[1] == 0x3):
                            #     # suste mode
                            # elif(data[1] == 0x4):
                            #     # thikka mode
                            # elif(data[1] == 0x5):
                            #     # babbal mode
                        
                        elif(data[0] == 0x5):
                            vehicleEvents.onStandSwitch(data[1])
                            # if(data[1] == 0x1):
                            #     # stand being used
                            # elif(data[1] == 0x2):
                            #     # stand no being used
                    if message.arbitration_id == 0x1E00100:
                        data=message.data
                        vehicleReadings.time(data)
                    if message.arbitration_id == 0x1E00102:
                        data=message.data
                        vehicleReadings.adxl(data)
                    
                    if message.arbitration_id == 0x1E00101:
                        data = message.data
                        vehicleReadings.vcuTemperature(data[1], data[0])
                    if message.arbitration_id == 0x1E00104:
                        data = message.data
                        current = round((data[1]*256 + data[2])*0.1, 2)
                        # print('Charging Current: ', current, 'A')
                        if(data[0] == 2):
                            isCharging = True
                            # print('Charging')
                        elif(data[0] == 1):
                            isCharging = False

                        if(isCharging != self.isCharging):
                            self.isCharging = isCharging
                            vehicleEvents.charging(self.isCharging, True)

    def onAutoOff(self, request):
        if(request == True):
            frame = can.Message(arbitration_id=0x1D00100, data=[1], extended_id=True)
            self.bus.send(frame)

    def startCAN(self):
        self.tExtractCANData = threading.Thread(target=self.extractCANData)
        self.tExtractCANData.start()

    def printData(self):
        while True:
            self.calculateRange()
            time.sleep(0.5)
            os.system('clear')
            print('Drive Mode                   : ', self.driveMode)
            print('Bike Speed                   : ', self.bikeSpeed, '      kmph')
            print('Time To Charge               : ', self.timeToCharge, '         min')
            print('Time To Discharge            : ', self.timeToDischarge, '         min')
            print('Distance Travelled           : ', self.odometer, '       km')
            print('Actual Torque                : ', self.actualTorque, '       Nm')
            print('State of Charge              : ', self.stateOfCharge, '      %')
            print('Battery Voltage              : ', self.packVoltage, '        V')
            print('Battery Status               : ', self.chargingStatus)
            print('Charging Current             : ', self.chargingCurrent, '        A')
            print('Discharging Current          : ', self.dischargingCurrent, '     A')
            print('Peak Charging Current        : ', self.peakChargingCurrent, '        A')
            print('Peak Discharging Current     : ', self.peakDischargingCurrent, '     A')
            print('Power                        : ', self.power, '                      hp')
            print('Remaining Capacity           : ', self.remainingCapacity, '          Ah')
            print('Range Thikka                 : ', self.rangeThikka, '          km')
            print('Range Suste                  : ', self.rangeSuste, '          km')
            print('Range Babbal                 : ', self.rangeBabbal, '          km')
    def calculateRange(self):
        # massBike                = 275               #kg
        # overallEfficiency       = 0.85
        # wheelRadius             = 1.94/(2*3.14)
        # avgSpeedInMeterThikka   = 12.5              #mps
        # avgSpeedInKmThikka      = 45                #kmph
        # avgSpeedInMeterSuste    = 8.33
        # avgSpeedInKmSuste       = 30
        # avgSpeedInMeterBabbal   = 20.8
        # avgSpeedInKmBabbal      = 75
        # acclDueToGravity        = 9.8               #m/s**2
        # rollingResistance       = 0.0030
        # airDensity              = 1.11
        # dragCoeff               = 0.70
        # area                    = 0.78
        # batteryFactor           = 1.00

        if((self.packVoltage==0)):
            return 0
        # Original Formula
        # power = (massBike * acclDueToGravity * avgSpeedInMeterThikka * rollingResistance) + (airDensity * dragCoeff * area * avgSpeedInMeterThikka**3)
        # wattHourPerKmThikka = power / avgSpeedInKmThikka
        # print('wattHourPerKmThikka: ', str(wattHourPerKmThikka))
        # Modified Formula
        # wattHourPerKmThikka = massBike * acclDueToGravity * rollingResistance / 3.6 + airDensity * dragCoeff * area * (avgSpeedInKmThikka**2) / 46.656
        # print('wattHourPerKmThikka: ', str(wattHourPerKmThikka))

        # Optimized Formula
        # wattHourPerKmThikka = 2.25 + 0.013*avgSpeedInKmThikka**2
        wattHourPerKmThikka = 28.575
        wattHourPerKmSuste = 13.95
        wattHourPerKmBabbal = 75.375
        # print('wattHourPerKmThikka: ', str(wattHourPerKmThikka))
        # AmpereHourPerKmThikka = wattHourPerKmThikka/self.packVoltage
        self.rangeThikka = int(self.remainingCapacity*self.packVoltage/wattHourPerKmThikka)
        self.rangeSuste = int(self.remainingCapacity*self.packVoltage/wattHourPerKmSuste)
        self.rangeBabbal = int(self.remainingCapacity*self.packVoltage/wattHourPerKmBabbal)

    def onGUIReady(self):
        vehicleReadings.socRange(self.stateOfCharge, self.stateOfHealth, self.rangeSuste, self.rangeSuste, self.rangeSuste)
        vehicleReadings.batteryTemperature(self.batteryTemperature)
        