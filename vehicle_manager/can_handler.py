import logging
import threading
import time
import can
import random
import os
from gui import *
from gpio_manager import GPIOWriter
from event_handler import *
import json
from stopwatch import Stopwatch

class CANHandler:
    def __init__(self, _gpioWriter):
    # def __init__(self):
        self.gpioWriter = _gpioWriter
        self.odoBeforeTrip          = 0     # km
        #Parameters
        self.chargingStatus         = 'discharging'
        self.chargingCurrent        = 0     # Ampere
        self.chargingCurrentCharger = 0     # Ampere
        self.packVoltage            = 0     # Volts
        self.stateOfCharge          = 0     # Percentage
        self.timeToCharge           = 0     # Minutes
        self.timeToDischarge        = 0     # Minutes
        self.highTemp               = 0     # Celsius      
        self.lowTemp                = 0     # Celsius
        self.bikeSpeed              = 0     # kmph
        self.maxTorque              = 0     # Newton-meter
        self.actualTorque           = 0     # Newton-meter
        self.motorTemp              = 0     # Celsius
        self.driveMode              = 0
        self.odometer               = 0     # km
        self.tripOdoOffset         = 0     # km
        self.tripOdo                = 0     # km
        self.peakChargingCurrent    = 0     # Ampere
        self.peakDischargingCurrent = 0     # Ampere
        self.dischargingCurrent     = 0     # Ampere
        self.power                  = 0     # W
        self.remainingCapacity      = 0     # Ampere-hour
        self.rangeThikka            = 0     # km
        self.rangeSuste             = 0     # km
        self.rangeBabbal            = 0     # km

        # BMS 18 Frame 2
        self.averageCurrent         = 0
        self.hiVoltModule           = 0
        self.hiVoltCell             = 0
        self.hiCellVolt             = 0
        self.lowVoltModule          = 0
        # BMS 18 Frame 3
        self.lowVoltCell            = 0
        self.lowCellVolt            = 0
        self.hiLowDiff              = 0
        self.highTempModule         = 0
        self.highTempNumber         = 0

        self.rideTime = 0
        self.initialRideTimeStatus = 0
        self.tripRideTimeOffset = 0
        self.tripSpeedInitial = 0
        self.maxBikeSpeed = 0
        #Configure CAN Interface
        can.rc['interface'] = 'socketcan_native'
        can.rc['channel'] = 'can0'
        self.bus = can.interface.Bus()

        #Configure logger
        logging.basicConfig(filename="can.log", format = '%(asctime)s - %(levelname)s - %(message)s', filemode='w')
        self.canLogger=logging.getLogger()
        self.canLogger.setLevel(logging.INFO)
        
        self.readTripData()
        #Start CAN
        self.stopwatch = Stopwatch()
        self.startCAN()

        #Subscribe to Trip Reset
        
        
        vehicleEvents.onTripReset += self.initiateTripReset

    def setChargingStatus(self, status):
        if(status != self.chargingStatus):
            print('Charge Status: ', status)
            self.chargingStatus = status
            vehicleEvents.onCharging(self.chargingStatus)

    def extractCANData(self):
        while True:
            message = self.bus.recv(0.1)
            if message is not None:
                if message.arbitration_id != 128:
                    if message.arbitration_id == 415236097:
                        data = message.data
                        #Battery Frame 0
                        if( (len(data) > 1) and (data[0] == 0)):
                            # print('Received Frame 0')
                            new_data=[data[0], data[2], data[1], data[4], data[3], data[6], data[5], data[7] ]

                            batteryStatus = (new_data[1]<<8) + new_data[2]
                            if((batteryStatus & 128) == 0):
                                self.setChargingStatus('discharging')
                            else:
                                self.setChargingStatus('charging')

                            self.packVoltage = int( ((new_data[3]<<8) + new_data[4])*0.1)
                            self.power = int(self.packVoltage * self.dischargingCurrent)
                            self.chargingCurrent = round(((new_data[5]<<8) + new_data[6])*0.01, 1)
                            
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 0:' + 'BatteryStatus : ' + str(self.chargingStatus)
                            self.canLogger.info(logMessage)
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 0:' + 'PackVoltage (V): ' + str(self.packVoltage)
                            self.canLogger.info(logMessage)
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 0:' + 'ChargingCurrent (A): ' + str(self.packVoltage)
                            self.canLogger.info(logMessage)
                        
                        #Battery Frame 1   
                        elif( (len(data) > 1) and (data[0] == 1)):
                            # print('Received Frame 1')
                            new_data=[data[0], data[2], data[1], data[4], data[3], data[6], data[5], data[7] ]

                            self.peakChargingCurrent = round(((new_data[1]<<8) + new_data[2])*0.01, 1)
                            self.dischargingCurrent = round(((new_data[3]<<8) + new_data[4])*0.01, 1)
                            self.peakDischargingCurrent = round(((new_data[5]<<8) + new_data[6])*0.01, 1)

                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 1:' + 'PeakChargingCurrent (A): ' + str(self.peakChargingCurrent)
                            self.canLogger.info(logMessage)
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 1:' + 'DischargingCurrent (A): ' + str(self.dischargingCurrent)
                            self.canLogger.info(logMessage)
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 1:' + 'PeakDIschargingCurrent (A): ' + str(self.peakDischargingCurrent)
                            self.canLogger.info(logMessage)

                        #Battery Frame 2
                        elif( (len(data) > 1) and (data[0] == 2)):
                            # print('Received Frame 2')
                            new_data=[data[0], data[2], data[1], data[3], data[4], data[6], data[5], data[7] ]

                            self.averageCurrent = round(((new_data[1]<<8) + new_data[2])*0.01, 1)
                            self.hiVoltModule = new_data[3]
                            self.hiVoltCell = new_data[4]
                            self.hiCellVolt = round(((new_data[5]<<8) + new_data[6]), 1)
                            self.lowVoltModule = new_data[7]
                            
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 2:' + 'AverageCurrent (A): ' + str(self.averageCurrent)
                            self.canLogger.info(logMessage)
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 2:' + 'ModuleNumberOfHighCellVolt : ' + str(self.hiVoltModule)
                            self.canLogger.info(logMessage)
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 2:' + 'CellNumberOfHighCellVolt : ' + str(self.hiVoltCell)
                            self.canLogger.info(logMessage)
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 2:' + 'HighCellVolt (mV): ' + str(self.hiCellVolt)
                            self.canLogger.info(logMessage)
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 2:' + 'ModuleNumberOfLowCellVolt : ' + str(self.lowVoltModule)
                            self.canLogger.info(logMessage)
                        #Battery Frame 3
                        elif( (len(data) > 1) and (data[0] == 3)):
                            # print('Received Frame 3')
                            new_data=[data[0], data[1], data[3], data[2], data[5], data[4], data[6], data[7] ]

                            self.lowVoltCell = new_data[1]
                            self.lowCellVolt = round(((new_data[2]<<8) + new_data[3]), 1)
                            self.hiLowDiff = round(((new_data[4]<<8) + new_data[5]), 1)
                            self.highTempModule = new_data[6]
                            self.highTempNumber = new_data[7]
                            
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 3:' + 'LowVoltCell : ' + str(self.lowVoltCell)
                            self.canLogger.info(logMessage)
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 3:' + 'LowCellVolt (mV): ' + str(self.lowCellVolt)
                            self.canLogger.info(logMessage)
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 3:' + 'HiLowDiff (mV): ' + str(self.hiLowDiff)
                            self.canLogger.info(logMessage)
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 3:' + 'HighTempModule : ' + str(self.highTempModule)
                            self.canLogger.info(logMessage)
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 3:' + 'HighTempNumber : ' + str(self.highTempNumber)
                            self.canLogger.info(logMessage)
                        #Battery Frame 4   
                        elif( (len(data) > 1) and (data[0] == 4)):
                            # print('Received Frame 4')
                            new_data=[data[0], data[2], data[1], data[3], data[4], data[6], data[5], data[7] ]

                            self.highTemp = int(((new_data[1]<<8) + new_data[2])*0.1)
                            self.lowTempModule = new_data[3]
                            self.lowTempNumber = new_data[4]
                            self.lowTemp = int(((new_data[5]<<8) + new_data[6])*0.1)
                            self.tempDiffLow = int(new_data[7]*0.1)

                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 4:' + 'HighTemp (C): ' + str(self.highTemp)
                            self.canLogger.info(logMessage)
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 4:' + 'lowTempModule : ' + str(self.lowTempModule)
                            self.canLogger.info(logMessage)
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 4:' + 'lowTempNumber : ' + str(self.lowTempNumber)
                            self.canLogger.info(logMessage)
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 4:' + 'lowTemp (C): ' + str(self.lowTemp)
                            self.canLogger.info(logMessage)
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 4:' + 'tempDiffLow (C): ' + str(self.tempDiffLow)
                            self.canLogger.info(logMessage)
                        
                        #Battery Frame 5
                        elif( (len(data) > 1) and (data[0] == 5)):
                            # print('Received Frame 5')
                            new_data=[data[0], data[1], data[3], data[2], data[5], data[4], data[7], data[6] ]
                            self.tempDiffHigh = int(new_data[1]*0.1)
                            self.stateOfCharge = int(((new_data[2]<<8) + new_data[3])*0.1)
                            self.remainingCapacity = int(((new_data[4]<<8) + new_data[5])*0.1)
                            self.timeToCharge = (new_data[6]<<8) + new_data[7]

                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 5:' + 'tempDiffHigh (C): ' + str(self.tempDiffHigh)
                            self.canLogger.info(logMessage)
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 5:' + 'stateOfCharge (%): ' + str(self.stateOfCharge)
                            self.canLogger.info(logMessage)
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 5:' + 'remainingCapacity (Ah): ' + str(self.remainingCapacity)
                            self.canLogger.info(logMessage)
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 5:' + 'timeToCharge (min): ' + str(self.timeToCharge)
                            self.canLogger.info(logMessage)

                        #Battery Frame 6
                        elif( (len(data) > 1) and (data[0] == 6)):
                            # print('Received Frame 6')
                            new_data=[data[0], data[2], data[1], data[4], data[3], data[6], data[5], data[7] ]

                            self.timeToDischarge = int(((new_data[1]<<8) + new_data[2]))
                            self.bmsOpVolt = int(((new_data[3]<<8) + new_data[4])*10)
                            self.bmsBoardTemp = int(((new_data[3]<<8) + new_data[4])*0.1)

                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 6:' + 'timeToDischarge (min): ' + str(self.timeToDischarge)
                            self.canLogger.info(logMessage)
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 6:' + 'bmsOpVolt (mV): ' + str(self.bmsOpVolt)
                            self.canLogger.info(logMessage)
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 6:' + 'bmsBoardTemp (C): ' + str(self.bmsBoardTemp)
                            self.canLogger.info(logMessage)
                        #Battery Frame 7
                        elif( (len(data) > 1) and (data[0] == 7)):
                            # print('Received Frame 7')
                            new_data=[data[0], data[2], data[1], data[4], data[3], data[6], data[5], data[7] ]

                            self.fullChargedCycle = int(((new_data[1]<<8) + new_data[2]))
                            self.fullDischargedCycle = int(((new_data[3]<<8) + new_data[4]))

                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 7:' + 'fullChargedCycle : ' + str(self.fullChargedCycle)
                            self.canLogger.info(logMessage)
                            logMessage = str(message.arbitration_id) + ' : '+ 'Frame 7:' + 'fullDischargedCycle : ' + str(self.fullDischargedCycle)
                            self.canLogger.info(logMessage)

                    elif message.arbitration_id == 663:
                        # Perform data swap in binary
                        data = message.data
                        new_data = [data[1], data[0], data[3], data[2], data[5], data[4], data[7], data[6]]
                        # Convert new_data to hex
                        count = 0
                        for d in new_data:
                            d_hex = hex(d)[2:]
                            new_data[count] = d_hex
                            count += 1
                        bat_current_hex = new_data[0] + new_data[1]
                        bat_voltage_hex = new_data[4] + new_data[5]
                        bat_current = int(int(bat_current_hex, 16)*0.0625)
                        #print('Battery Current from Motor: ', bat_current)
                        bat_voltage = int(int(bat_voltage_hex, 16)*0.0625)
                        bat_v_notint = int(bat_voltage_hex, 16)*0.0625
                        # Fix negative current issue
                        if bat_current > 4096/2:
                            bat_current = int(bat_current - 4096)
                            recuperation = 1
                        else:
                            recuperation = 0
                        self.dischargingCurrent = bat_current
                        self.power = int(self.packVoltage * self.dischargingCurrent)
                        # Calculate Battery SoC and Range
                        s_o_charge = int((bat_v_notint - 95.12) / (101.2 - 95.12) * 100)
                        if s_o_charge < 0:
                            s_o_charge = 0
                        elif s_o_charge > 100:
                            s_o_charge = 100
                        est_range = s_o_charge * 1.5  # Assuming 150km when 100%
                        #logMessage = 'Frame:    663' + ' - ' + 'DischargingCurrent:  ' + str(self.dischargingCurrent) + ' A - ' + 'Power:   '+str(self.power) 
                        #print(logMessage)
                        #self.canLogger.warning(logMessage)
                    # Motor Controller
                    elif message.arbitration_id == 1024:
                        # Perform data swap in binary
                        data = message.data
                        new_data = [data[1], data[0], data[3], data[2], data[5], data[4], data[7], data[6]]
                        self.bikeSpeed = int(((new_data[0]<<8) + new_data[1])*0.0625)

                        self.maxTorque = round(((new_data[2]<<8) + new_data[3])*0.1, 1)
                        self.actualTorque = round(((new_data[4]<<8) + new_data[5])*0.0625, 1)
                        self.motorTemp = round(((new_data[6]<<8) + new_data[7]), 1)
                        # Fix negative velocity issue
                        if self.bikeSpeed > 4096/2:
                            self.bikeSpeed = 0
                        vehicleReadings.speedReading(self.bikeSpeed)

                        if(self.bikeSpeed > 5):
                            if(not self.stopwatch.running):
                                self.stopwatch.start()
                        else:
                            if(self.stopwatch.running):
                                self.stopwatch.stop()
                                self.rideTime = self.stopwatch.duration
                        
                        if((self.bikeSpeed > self.maxBikeSpeed)):
                            self.maxBikeSpeed = self.bikeSpeed
                        
                        # Fix negative torque issue
                        if self.actualTorque > 4096/2:
                            self.actualTorque = int(self.actualTorque-4096)
                        #logMessage = 'Frame:    1024' + ' - ' + 'BikeSpeed:  ' + str(self.bikeSpeed) + ' rpm - ActualTorque:   ' + str(self.actualTorque) + ' Nm '
                        #print(logMessage)
                        #self.canLogger.info(logMessage)
                    elif message.arbitration_id == 336:
                        # Perform data swap in binary
                        data = message.data
                        new_data = [data[1], data[0], data[3], data[2], data[5], data[4], data[7], data[6]]
                        # Convert new_data to hex
                        count = 0
                        for d in new_data:
                            d_hex = hex(d)[2:]
                            new_data[count] = d_hex
                            count += 1
                        motor_vel_hex = new_data[6] + new_data[7] + new_data[4] + new_data[5]
                        motor_vel = int(motor_vel_hex, 16)*1
                        # Fix negative motor rpm issue
                        if motor_vel > 4294967295/2:  # 4294967295 is 'ffffffff' in hex
                            motor_vel = 0
                    elif message.arbitration_id == 664:
                        # Perform data swap in binary
                        data = message.data
                        new_data = [data[1], data[0], data[3], data[2]]
                        # Convert new_data to hex
                        count = 0
                        for d in new_data:
                            d_hex = hex(d)[2:]
                            new_data[count] = d_hex
                            count += 1
                        drive_prof_hex = new_data[0] + new_data[1]
                        drive_prof = int(drive_prof_hex, 16)*1
                        self.driveMode = drive_prof
                        #logMessage = 'Frame:    664' + ' - ' + 'DriveMode:  ' + str(drive_prof)
                        #print(logMessage)
                       # self.canLogger.info(logMessage)
                    elif message.arbitration_id == 769:
                        # Perform data swap in binary
                        data = message.data
                        new_data = [data[1], data[0], data[3], data[2], data[5], data[4], data[7], data[6]]
                        # Convert new_data to hex
                        count = 0
                        for d in new_data:
                            d_hex = hex(d)[2:]
                            new_data[count] = d_hex
                            count += 1
                        odometer_hex = new_data[2] + new_data[3] + new_data[0] + new_data[1]
                        htsink_temp_hex = new_data[7]
                        dig_input_hex = new_data[6]
                        odometer = int(int(odometer_hex, 16)*0.0039)
                        self.odometer = odometer
                        vehicleReading.odoReading(self.odometer)

                        htsink_temp = int(int(htsink_temp_hex, 16)*1)
                        dig_input = int(int(dig_input_hex, 16)*1)
                        # self.initializeRideTime()
                        if(not self.initialRideTimeStatus):
                            self.initializeRideTime()
                        #logMessage = 'Frame:    769' + ' - ' + 'Odometer:  ' + str(odometer) + ' km'
                        #print(logMessage)
                        # self.canLogger.info(logMessage)
                    elif message.arbitration_id == 773:
                        data = message.data
                        new_data = [data[0], data[2], data[1], data[4], data[3], data[6], data[5], data[7]]
                        self.chargingCurrentCharger = round(((new_data[3]<<8) + new_data[4])*0.1, 1)
                        self.canLogger.warning(self.chargingCurrentCharger)
                    elif message.arbitration_id == 768:
                        data=message.data
                        #new_data = [data[0], data[2], data[1], data[4], data[3], data[6], data[5], data[7]]
                        self.canLogger.warning('Charging Command')

    def requestCANFrames(self):
        while True:
            frame = can.Message(arbitration_id=0x18C00001,data=[0], extended_id=True)
            self.bus.send(frame)
            time.sleep(0.1)
            frame = can.Message(arbitration_id=0x18C00001,data=[1], extended_id=True)
            self.bus.send(frame)
            time.sleep(0.1)
            frame = can.Message(arbitration_id=0x18C00001,data=[2], extended_id=True)
            self.bus.send(frame)
            time.sleep(0.1)
            frame = can.Message(arbitration_id=0x18C00001,data=[3], extended_id=True)
            self.bus.send(frame)
            time.sleep(0.1)
            frame = can.Message(arbitration_id=0x18C00001,data=[4], extended_id=True)
            self.bus.send(frame)
            time.sleep(0.1)
            frame = can.Message(arbitration_id=0x18C00001,data=[5], extended_id=True)
            self.bus.send(frame)
            time.sleep(0.1)
            frame = can.Message(arbitration_id=0x18C00001,data=[6], extended_id=True)
            self.bus.send(frame)
            time.sleep(0.1)
            frame = can.Message(arbitration_id=0x18C00001,data=[7], extended_id=True)
            self.bus.send(frame)
            time.sleep(0.3)
    def startFastCharge(self):
        print('Starting Fast Charging')
        count = 0
        while(count < 1000):
            # print('Fast Charging')
            os.system('cansend can0 300#01E8034C040500')
            count = count + 1
    # def requestFastCharge(self):
    #         frame = can.Message(arbitration_id=0x300,data=[01 E8 03 4C 04 AA 00], extended_id=False)
    #         self.bus.send(frame)
    #         time.sleep(0.1)

    def pushFastData(self):
        while True:
            time.sleep(0.2)
            publishSpeedPower(self.bikeSpeed, self.power)
            publishChargingStatus(self.chargingStatus, self.chargingCurrent, self.timeToCharge)
            #self.startFastCharge()

    def pushSlowData(self):
        while True:
            self.calculateRange()
            self.computeTripOdo()
            if(self.initialRideTimeStatus):
                self.computeAverageSpeed()
                publishSpeedInfograph(self.maxBikeSpeed, self.averageSpeed, self.tripAverageSpeed)
            publishSOC(self.stateOfCharge, self.rangeSuste, self.rangeThikka, self.rangeBabbal)
            publishOdometer(self.odometer, self.tripOdo)
            # publishRange(self.rangeSuste, self.rangeThikka, self.rangeBabbal)
            #self.stateOfCharge = 55
            # print('SOC: ', self.stateOfCharge)
            # self.gpioWriter.setSOC(self.stateOfCharge)
            time.sleep(1)
    
    def startCAN(self):
        self.tExtractCANData = threading.Thread(target=self.extractCANData)
        self.tExtractCANData.start()
        self.tRequestFrames = threading.Thread(target=self.requestCANFrames)
        self.tRequestFrames.start()
        self.tPushFastData = threading.Thread(target=self.pushFastData)
        self.tPushFastData.start()
        self.tPushSlowData = threading.Thread(target=self.pushSlowData)
        self.tPushSlowData.start()
        self.tPrintData = threading.Thread(target=self.printData)
        #self.tPrintData.start()

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
    
    def initiateTripReset(self):
        tripReset = {
            'tripDistanceOffsetOnBoot': self.odometer,
            'averageTripSpeedOnBoot': 0
        }
        with open('trip.json', 'w') as f:  # writing JSON object
            json.dump(tripReset, f)
        self.tripOdoOffset = self.odometer
        self.tripOdo = 0
        self.tripRideTimeOffset = self.stopwatch.duration/3600 + self.initialTripRideTIme 
        publishOdometer(self.odometer, self.tripOdo)
    
    def computeTripOdo(self):
        self.tripOdo = self.odometer - self.tripOdoOffset
        # self.tripRideTime = self.stopwatch.duration


    def readTripData(self):
        with open('trip.json', 'r') as f:
            self.tripData = json.load(f)
        self.tripOdoOffset = self.tripData['tripDistanceOffsetOnBoot']
        self.tripSpeedInitial = self.tripData['averageTripSpeedOnBoot']

        with open('speed.json', 'r') as f:
            speed = json.load(f)
            self.averageSpeed = speed['odoAverageSpeedOnBoot']
            self.maxBikeSpeed = speed['maxSpeedOnBoot']
        print('tripOdoOffset: ', str(self.tripOdoOffset))
        print('tripSpeedInitial: ', str(self.tripSpeedInitial))
        print('Average Speed On Boot: ', str(self.averageSpeed))
        print('Max Speed On Boot: ', str(self.maxBikeSpeed))

    
    def initializeRideTime(self):
        self.initialRideTime = self.odometer / self.averageSpeed
        print('InitialRideTime: ', str(self.initialRideTime))
        self.computeTripOdo()
        self.initialTripRideTime = self.tripOdo / self.tripSpeedInitial
        print('initialTripRideTime: ', str(self.initialTripRideTime))
        self.initialRideTimeStatus = 1

    def computeAverageSpeed(self):
        self.averageSpeed = self.odometer / (self.initialRideTime + self.stopwatch.duration/3600)
        # print('Total Distance: ', str(self.odometer))
        # print('Ride Time: ', str(self.rideTime))
        # print('Average Speed: ', str(self.averageSpeed))

        self.computeTripOdo()
        self.tripRideTime = (self.stopwatch.duration / 3600) + self.initialTripRideTime - self.tripRideTimeOffset
        self.tripAverageSpeed = self.tripOdo / self.tripRideTime
        # print('initialTripRideTime: ', str(self.initialTripRideTime))
        # print('tripRideTime: ', str(self.tripRideTime))
        # print('Trip Average Speed: ', str(self.tripAverageSpeed))
        # print('Trip Average Speed: ', str(self.tripAverageSpeed))