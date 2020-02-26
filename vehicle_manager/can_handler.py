import logging
import threading
import time
import can
import random
import os
from gui import *
from gpio_manager import GPIOWriter
from event_handler import *
from mqtt_publisher import *
class CANHandler:
    # def __init__(self, _gpioWriter):
    def __init__(self):
        # self.gpioWriter = _gpioWriter
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
        self.batteryTemperature     = 0     # Celsius
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
        #Lith-Tech Battery
        self.batteryCurrent         = 0
        self.batteryVoltage         = 0
        #Configure CAN Interface
        can.rc['interface'] = 'socketcan_native'
        can.rc['channel'] = 'can0'
        self.bus = can.interface.Bus()    

        #Configure logger
        LOG_FILENAME = "yatri.log"
        # logging.basicConfig(filename=LOG_FILENAME, format = '%(asctime)s : %(name)s : %(levelname)s : %(message)s', filemode='a')
        # logging.basicConfig(filemode='a')
        LOG_FORMAT = ('%(asctime)s : %(name)s : %(levelname)s : %(message)s')
        self.canLogger=logging.getLogger("event_logger")
        self.canLogger.setLevel(logging.INFO)
        self.canLoggerHandler = logging.FileHandler('../logs/yatri.log')
        self.canLoggerHandler.setLevel(logging.INFO)
        self.canLoggerHandler.setFormatter(logging.Formatter(LOG_FORMAT))
        self.canLogger.addHandler(self.canLoggerHandler)

        self.dataLogger=logging.getLogger("periodic_logger")
        self.dataLogger.setLevel(logging.INFO)
        self.dataLoggerHandler = logging.FileHandler('../logs/data-log.log')
        self.dataLoggerHandler.setLevel(logging.INFO)
        self.dataLoggerHandler.setFormatter(logging.Formatter('%(asctime)s : %(message)s'))
        self.dataLogger.addHandler(self.dataLoggerHandler)

        message = 'StateOfCharge(%)' + ' : ' + 'BikeSpeed(kmph)' + ' : ' + 'MotorCurrent(A)' + ' : ' + 'MotorVoltage(V)' + ' : ' + 'ActualTorque(Nm)'  + ' : ' + 'Odometer(km)'
        self.dataLogger.info(message)
        # Add the log message handler to the logger
        #handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=2048, backupCount=10)

        #self.canLogger.addHandler(handler)
        #Start CAN
        self.startCAN()
        vehicleEvents.onBLEReady += self.onBLEReady

    def setChargingStatus(self, status):
        if(status != self.chargingStatus):
            print('Charge Status: ', status)
            self.chargingStatus = status
            vehicleEvents.onCharging(self.chargingStatus)
    def onBLEReady(self, value):
        # print('BLE is ready.')
        if(value == 1):
            vehicleReadings.batteryStatus(self.stateOfCharge)
    def extractCANData(self):
        while True:
            message = self.bus.recv(0.1)
            if message is not None:
                if message.arbitration_id != 128:
                    #Lith-Tech Battery
                    if message.arbitration_id == 284693918:
                        data = message.data
                        new_data=[data[0], data[1], data[2], data[4], data[3], data[6], data[5], data[7] ]
                        batteryStatus = new_data[0]
                        if((batteryStatus & 273) == 0):
                            self.setChargingStatus('discharging')
                        else:
                            self.setChargingStatus('charging')
                        
                        batteryTempOld = self.batteryTemperature
                        tempStateOfCharge = self.stateOfCharge
                        self.batteryTemperature = int(new_data[1]) - 40
                        self.stateOfCharge = round(new_data[2], 2)
                        self.batteryCurrent = round(((new_data[3]<<8) + new_data[4]) * 0.05, 2) - 1600
                        self.batteryVoltage = round(((new_data[5]<<8) + new_data[6]) * 0.1, 2)
                        self.power = self.batteryCurrent * self.batteryPower / 746

                        if(tempStateOfCharge != self.stateOfCharge):
                            vehicleReadings.batteryStatus(self.stateOfCharge)
                        if batteryTempOld != self.batteryTemperature:
                            vehicleReadings.batteryTemperature(self.batteryTemperature)
                        # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 1:' + 'ChargingStatus : ' + str(self.chargingStatus)
                        # self.canLogger.info(logMessage)
                        # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 1:' + 'batteryTemperature : ' + str(self.batteryTemperature)
                        # self.canLogger.info(logMessage)
                        # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 1:' + 'stateOfCharge : ' + str(self.stateOfCharge)
                        # self.canLogger.info(logMessage)
                        # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 1:' + 'batteryCurrent : ' + str(self.batteryCurrent)
                        # self.canLogger.info(logMessage)
                        # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 1:' + 'batteryVoltage : ' + str(self.batteryVoltage)
                        # self.canLogger.info(logMessage)
                        # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 1:' + 'batteryVoltage : ' + str(self.power)
                        # self.canLogger.info(logMessage)
                        logMessage = 'LithTech3.3kWh :' + str(message.arbitration_id) + ' : '+ 'Frame 1:' + 'ChargingStatus : ' + str(self.chargingStatus) + ' : ' + 'batteryTemperature : ' + str(self.batteryTemperature) + ' : ' + 'stateOfCharge : ' + str(self.stateOfCharge) + ' : ' + 'batteryCurrent : ' + str(self.batteryCurrent) + ' : ' + 'batteryVoltage : ' + str(self.batteryVoltage) + + ' : '+ 'Frame 1:' + 'batteryVoltage : ' + str(self.power)
                        self.canLogger.info(logMessage)

                    #Lith-Tech Battery
                    elif message.arbitration_id == 418649071:
                        data = message.data
                        new_data=[data[0], data[1], data[2], data[4], data[3], data[6], data[5], data[7] ]
                        soc = round(((data[5]<<8) + data[4])*0.1,1)
                        if(soc != self.stateOfCharge):
                            self.stateOfCharge = soc
                            vehicleReadings.batteryStatus(self.stateOfCharge)
                        logMessage = 'LithTech5.7kWh :' + str(message.arbitration_id) + ' : '+'stateOfCharge : ' + str(self.stateOfCharge)
                        self.canLogger.info(logMessage)
                    elif message.arbitration_id == 415236097:
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

                            packVoltageOld = self.packVoltage
                            self.packVoltage = round( ((new_data[3]<<8) + new_data[4])*0.1, 2)
                            # self.power = round(self.packVoltage * self.dischargingCurrent, 2)
                            self.chargingCurrent = round(((new_data[5]<<8) + new_data[6])*0.01, 2)
                            if(packVoltageOld != self.packVoltage):
                                vehicleReadings.packVoltage(self.packVoltage)
                            logMessage = 'KoKam :' + str(message.arbitration_id) + ' : '+ 'Frame 0:' + 'BatteryStatus: ' + str(self.chargingStatus) + ' : '+ 'PackVoltage(V): ' + str(self.packVoltage)+ ' : ' + 'ChargingCurrent(A): ' + str(self.packVoltage)
                            self.canLogger.info(logMessage)
                        
                        #Battery Frame 1   
                        elif( (len(data) > 1) and (data[0] == 1)):
                            # print('Received Frame 1')
                            new_data=[data[0], data[2], data[1], data[4], data[3], data[6], data[5], data[7] ]

                            self.peakChargingCurrent = round(((new_data[1]<<8) + new_data[2])*0.01, 2)
                            # self.dischargingCurrent = round(((new_data[3]<<8) + new_data[4])*0.01, 2)
                            self.peakDischargingCurrent = round(((new_data[5]<<8) + new_data[6])*0.01, 2)

                            logMessage = 'KoKam :' + str(message.arbitration_id) + ' : '+ 'Frame 1:' + 'PeakChargingCurrent(A): ' + str(self.peakChargingCurrent) + ' : '+ 'PeakDischargingCurrent(A): ' + str(self.peakDischargingCurrent) + ' : '+ 'DischargingCurrent (A): ' + str(self.dischargingCurrent)
                            self.canLogger.info(logMessage)
                            # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 1:' + 'DischargingCurrent (A): ' + str(self.dischargingCurrent)
                            # self.canLogger.info(logMessage)
                            # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 1:' + 'PeakDischargingCurrent(A): ' + str(self.peakDischargingCurrent)
                            # self.canLogger.info(logMessage)

                        #Battery Frame 2
                        elif( (len(data) > 1) and (data[0] == 2)):
                            # print('Received Frame 2')
                            new_data=[data[0], data[2], data[1], data[3], data[4], data[6], data[5], data[7] ]

                            self.averageCurrent = round(((new_data[1]<<8) + new_data[2])*0.01, 2)
                            self.hiVoltModule = new_data[3]
                            self.hiVoltCell = new_data[4]
                            self.hiCellVolt = round(((new_data[5]<<8) + new_data[6]), 2)
                            self.lowVoltModule = new_data[7]
                            
                            # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 2:' + 'AverageCurrent (A): ' + str(self.averageCurrent)
                            # self.canLogger.info(logMessage)
                            logMessage = 'KoKam :' + str(message.arbitration_id) + ' : '+ 'Frame 2:' + 'AverageCurrent (A): ' + str(self.averageCurrent)+' : '+ 'ModuleNumberOfHighCellVolt : ' + str(self.hiVoltModule)+ ' : ' + 'CellNumberOfHighCellVolt : ' + str(self.hiVoltCell) + ' : '+ 'HighCellVolt (mV): ' + str(self.hiCellVolt) + ' : '+ 'ModuleNumberOfLowCellVolt : ' + str(self.lowVoltModule)
                            self.canLogger.debug(logMessage)
                            # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 2:' + 'CellNumberOfHighCellVolt : ' + str(self.hiVoltCell)
                            # self.canLogger.info(logMessage)
                            # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 2:' + 'HighCellVolt (mV): ' + str(self.hiCellVolt)
                            # self.canLogger.info(logMessage)
                            # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 2:' + 'ModuleNumberOfLowCellVolt : ' + str(self.lowVoltModule)
                            # self.canLogger.info(logMessage)
                        #Battery Frame 3
                        elif( (len(data) > 1) and (data[0] == 3)):
                            # print('Received Frame 3')
                            new_data=[data[0], data[1], data[3], data[2], data[5], data[4], data[6], data[7] ]

                            self.lowVoltCell = new_data[1]
                            self.lowCellVolt = round(((new_data[2]<<8) + new_data[3]), 2)
                            self.hiLowDiff = round(((new_data[4]<<8) + new_data[5]), 2)
                            self.highTempModule = new_data[6]
                            self.highTempNumber = new_data[7]
                            
                            logMessage = 'KoKam :' + str(message.arbitration_id) + ' : '+ 'Frame 3:' + 'LowVoltCell : ' + str(self.lowVoltCell)+ ' : ' + 'LowCellVolt (mV): ' + str(self.lowCellVolt)+ ' : '+ 'HiLowDiff (mV): ' + str(self.hiLowDiff)+ ' : '+ 'HighTempModule : ' + str(self.highTempModule)+ ' : '+ 'HighTempNumber : ' + str(self.highTempNumber)
                            self.canLogger.debug(logMessage)
                            # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 3:' + 'LowCellVolt (mV): ' + str(self.lowCellVolt)
                            # self.canLogger.info(logMessage)
                            # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 3:' + 'HiLowDiff (mV): ' + str(self.hiLowDiff)
                            # self.canLogger.info(logMessage)
                            # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 3:' + 'HighTempModule : ' + str(self.highTempModule)
                            # self.canLogger.info(logMessage)
                            # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 3:' + 'HighTempNumber : ' + str(self.highTempNumber)
                            # self.canLogger.info(logMessage)
                        #Battery Frame 4   
                        elif( (len(data) > 1) and (data[0] == 4)):
                            # print('Received Frame 4')
                            new_data=[data[0], data[2], data[1], data[3], data[4], data[6], data[5], data[7] ]
                            highTempOld = self.highTemp
                            self.highTemp = round(((new_data[1]<<8) + new_data[2])*0.1, 2)
                            self.lowTempModule = new_data[3]
                            self.lowTempNumber = new_data[4]
                            self.lowTemp = round(((new_data[5]<<8) + new_data[6])*0.1, 2)
                            self.tempDiffLow = round(new_data[7]*0.1, 2)
                            if(highTempOld != self.highTemp): 
                                vehicleReadings.batteryTemperature(self.highTemp)
                            logMessage = 'KoKam :' + str(message.arbitration_id) + ' : '+ 'Frame 4:' + 'HighTemp (C): ' + str(self.highTemp)+ ' : '+ 'lowTempModule : ' + str(self.lowTempModule)+ ' : ' + 'lowTempNumber : ' + str(self.lowTempNumber)+ ' : '+ 'lowTemp (C): ' + str(self.lowTemp)+ ' : '+ 'tempDiffLow (C): ' + str(self.tempDiffLow)
                            self.canLogger.debug(logMessage)
                            # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 4:' + 'lowTempModule : ' + str(self.lowTempModule)
                            # self.canLogger.info(logMessage)
                            # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 4:' + 'lowTempNumber : ' + str(self.lowTempNumber)
                            # self.canLogger.info(logMessage)
                            # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 4:' + 'lowTemp (C): ' + str(self.lowTemp)
                            # self.canLogger.info(logMessage)
                            # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 4:' + 'tempDiffLow (C): ' + str(self.tempDiffLow)
                            # self.canLogger.info(logMessage)
                        
                        #Battery Frame 5
                        elif( (len(data) > 1) and (data[0] == 5)):
                            # print('Received Frame 5')
                            tempStateOfCharge = self.stateOfCharge

                            new_data=[data[0], data[1], data[3], data[2], data[5], data[4], data[7], data[6] ]
                            self.tempDiffHigh = round(new_data[1]*0.1, 2)
                            self.stateOfCharge = round(((new_data[2]<<8) + new_data[3])*0.1, 2)
                            self.remainingCapacity = round(((new_data[4]<<8) + new_data[5])*0.1, 2)
                            self.timeToCharge = (new_data[6]<<8) + new_data[7]

                            if(tempStateOfCharge != self.stateOfCharge):
                                vehicleReadings.batteryStatus(self.stateOfCharge)
                            logMessage = 'KoKam :' + str(message.arbitration_id) + ' : '+ 'Frame 5:' + 'tempDiffHigh (C): ' + str(self.tempDiffHigh)+ ' : ' + 'stateOfCharge (%): ' + str(self.stateOfCharge)+ ' : '+ 'remainingCapacity (Ah): ' + str(self.remainingCapacity)+ ' : '+ 'timeToCharge (min): ' + str(self.timeToCharge)
                            self.canLogger.info(logMessage)
                            # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 5:' + 'stateOfCharge (%): ' + str(self.stateOfCharge)
                            # self.canLogger.info(logMessage)
                            # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 5:' + 'remainingCapacity (Ah): ' + str(self.remainingCapacity)
                            # self.canLogger.info(logMessage)
                            # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 5:' + 'timeToCharge (min): ' + str(self.timeToCharge)
                            # self.canLogger.info(logMessage)

                        #Battery Frame 6
                        elif( (len(data) > 1) and (data[0] == 6)):
                            # print('Received Frame 6')
                            new_data=[data[0], data[2], data[1], data[4], data[3], data[6], data[5], data[7] ]

                            self.timeToDischarge = round(((new_data[1]<<8) + new_data[2]), 2)
                            self.bmsOpVolt = round(((new_data[3]<<8) + new_data[4])*10, 2)
                            self.bmsBoardTemp = round(((new_data[3]<<8) + new_data[4])*0.1, 2)

                            logMessage = 'KoKam :' + str(message.arbitration_id) + ' : '+ 'Frame 6:' + 'timeToDischarge (min): ' + str(self.timeToDischarge)+ ' : '+ 'bmsOpVolt (mV): ' + str(self.bmsOpVolt)+ ' : '+ 'bmsBoardTemp (C): ' + str(self.bmsBoardTemp)
                            self.canLogger.info(logMessage)
                            # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 6:' + 'bmsOpVolt (mV): ' + str(self.bmsOpVolt)
                            # self.canLogger.info(logMessage)
                            # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 6:' + 'bmsBoardTemp (C): ' + str(self.bmsBoardTemp)
                            # self.canLogger.info(logMessage)
                        #Battery Frame 7
                        elif( (len(data) > 1) and (data[0] == 7)):
                            # print('Received Frame 7')
                            new_data=[data[0], data[2], data[1], data[4], data[3], data[6], data[5], data[7] ]

                            self.fullChargedCycle = round(((new_data[1]<<8) + new_data[2]), 2)
                            self.fullDischargedCycle = round(((new_data[3]<<8) + new_data[4]), 2)

                            logMessage = 'KoKam :' + str(message.arbitration_id) + ' : '+ 'Frame 7:' + 'fullChargedCycle : ' + str(self.fullChargedCycle) + ' : '+ 'fullDischargedCycle : ' + str(self.fullDischargedCycle)
                            self.canLogger.debug(logMessage)
                            # logMessage = str(message.arbitration_id) + ' : '+ 'Frame 7:' + 'fullDischargedCycle : ' + str(self.fullDischargedCycle)
                            # self.canLogger.info(logMessage)

                    elif message.arbitration_id == 663:
                        # Perform data swap in binary
                        data = message.data
                        new_data = [data[1], data[0], data[3], data[2], data[5], data[4], data[7], data[6]]
                        bat_current = round(((new_data[0]<<8) + new_data[1])*0.0625,2)
                        # Convert new_data to hex
                        count = 0
                        for d in new_data:
                            d_hex = hex(d)[2:]
                            new_data[count] = d_hex
                            count += 1
                        #bat_current_hex = new_data[0] + new_data[1]
                        bat_voltage_hex = new_data[4] + new_data[5]
                        #bat_current = round(int(bat_current_hex, 16)*0.0625, 2)
                        #print('Battery Current from Motor: ', bat_current)
                        bat_voltage = round(int(bat_voltage_hex, 16)*0.0625, 2)
                        bat_v_notint = round(int(bat_voltage_hex, 16)*0.0625, 2)
                        # Fix negative current issue
                        if bat_current > 4096/2:
                            bat_current = round(bat_current - 4096, 2)
                            recuperation = 1
                        else:
                            recuperation = 0
                        self.dischargingCurrent = bat_current
                        #self.power = int(self.packVoltage * self.dischargingCurrent / 746)
                        self.power = round(bat_current * bat_v_notint / 746, 2)
                        self.motorCurrent = bat_current
                        self.motorVoltage = bat_v_notint
                        # el-psy-congroo
                        # this following line is used as a debug feature as BMS CAN
                        # is not working with Controller CAN at the moment
                        # when Lith-Tech Battery is being used
                        # tempStateOfCharge = self.stateOfCharge
                        # self.stateOfCharge = int(bat_v_notint)
                        # if(tempStateOfCharge != self.stateOfCharge):
                        #     vehicleReadings.batteryStatus(self.stateOfCharge)
                        # Calculate Battery SoC and Range
                        s_o_charge = round((bat_v_notint - 95.12) / (101.2 - 95.12) * 100, 2)
                        if s_o_charge < 0:
                            s_o_charge = 0
                        elif s_o_charge > 100:
                            s_o_charge = 100
                        est_range = s_o_charge * 1.5  # Assuming 150km when 100%
                        #logMessage = 'Frame:    663' + ' - ' + 'DischargingCurrent:  ' + str(self.dischargingCurrent) + ' A - ' + 'Power:   '+str(self.power) 
                        #print(logMessage)
                        #self.canLogger.warning(logMessage)
                        # logMessage = str(message.arbitration_id) + ' : '+ 'Frame NA:' + 'Motor Battery Voltage : ' + str(int(bat_v_notint))
                        logMessage = 'Motor :' + str(message.arbitration_id) + ' : '+ 'Motor Battery Voltage : ' + str(bat_v_notint) + ' : '+ 'Motor Battery Current : ' + str(self.dischargingCurrent) + ' : '+ 'Motor Power : ' + str(self.power)
                        self.canLogger.info(logMessage)
                        # logMessage = str(message.arbitration_id) + ' : '+ 'Frame NA:' + 'Motor Battery Current : ' + str(self.dischargingCurrent)
                        # self.canLogger.info(logMessage)
                        # logMessage = str(message.arbitration_id) + ' : '+ 'Frame NA:' + 'Motor Power : ' + str(self.power)
                        # self.canLogger.info(logMessage)
                    # Motor Controller
                    elif message.arbitration_id == 1024:
                        # Perform data swap in binary
                        data = message.data
                        new_data = [data[1], data[0], data[3], data[2], data[5], data[4], data[7], data[6]]
                        speed = round(((new_data[0]<<8) + new_data[1])*0.0625, 2)
                        # Fix negative velocity issue
                        if speed > 4096/2:
                            self.bikeSpeed = 0
                        else:
                            self.bikeSpeed = speed
                        self.maxTorque = round(((new_data[2]<<8) + new_data[3])*0.1, 2)
                        self.actualTorque = round(((new_data[4]<<8) + new_data[5])*0.0625, 2)
                        motorTemp = round(((new_data[6]<<8) + new_data[7]), 2)
                        if(motorTemp != self.motorTemp):
                            self.motorTemp = motorTemp
                            vehicleReadings.motorTemperature(self.motorTemp)

                        vehicleReadings.speedReading(self.bikeSpeed)

                        # Fix negative torque issue
                        if self.actualTorque > 4096/2:
                            self.actualTorque = round(self.actualTorque-4096, 2)
                        #logMessage = 'Frame:    1024' + ' - ' + 'BikeSpeed:  ' + str(self.bikeSpeed) + ' rpm - ActualTorque:   ' + str(self.actualTorque) + ' Nm '
                        #print(logMessage)
                        #self.canLogger.info(logMessage)
                        logMessage = 'Motor :' + str(message.arbitration_id) + ' : '+ 'BikeSpeed(kmph): ' + str(self.bikeSpeed) + ' : '+ 'MaxTorque(Nm): ' + str(self.maxTorque) + ' : '+'ActualTorque(Nm): ' + str(self.actualTorque)
                        self.canLogger.info(logMessage)
                        # logMessage = str(message.arbitration_id) + ' : '+ 'Frame NA:' + 'MaxTorque (Nm): ' + str(self.maxTorque)
                        # self.canLogger.warning(logMessage)
                        # logMessage = str(message.arbitration_id) + ' : '+ 'Frame NA:' + 'ActualTorque (Nm): ' + str(self.actualTorque)
                        # self.canLogger.warning(logMessage)
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

                        motor_spd_hex = new_data[2] + new_data[3] + new_data[0] + new_data[1]
                        motor_spd = int(motor_spd_hex, 16)*1
                        # Fix negative motor rpm issue
                        if motor_spd > 4294967295/2:  # 4294967295 is 'ffffffff' in hex
                            motor_spd = 0
                        logMessage = 'KoKam :' + str(message.arbitration_id) + ' : '+ 'MaxMotorSpeed (NA): ' + str(motor_spd) + ' : '+ 'MaxMotorVelocity (rpm): ' + str(motor_vel)
                        self.canLogger.info(logMessage)
                        # logMessage = str(message.arbitration_id) + ' : '+ 'Frame NA:' + 'MaxMotorVelocity (rpm): ' + str(motor_vel)
                        # self.canLogger.warning(logMessage)
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
                        # print(data)
                        new_data = [data[1], data[0], data[3], data[2], data[5], data[4], data[7], data[6]]
                        new_new_data = [data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]]
                        # Convert new_data to hex
                        count = 0
                        for d in new_data:
                            d_hex = hex(d)[2:]
                            new_data[count] = d_hex
                            count += 1
                        odometer_hex = new_data[2] + new_data[3] + new_data[0] + new_data[1]
                        htsink_temp_hex = new_data[7]
                        dig_input_hex = new_data[6]
                        # odometer = int(int(odometer_hex, 16)*0.0039)
                        odometer = round(((new_new_data[3] << 24) +(new_new_data[2] << 16) +(new_new_data[1] << 8) + new_new_data[0])*0.0039, 2)
                        # odometer = uint((new_new_data[3] << 24 + new_new_data[2]<<16 + new_new_data[1]<<8 + new_new_data[0]) * 0.0039)
                        self.odometer = odometer
                        vehicleReadings.odoReading(self.odometer)

                        htsink_temp = int(int(htsink_temp_hex, 16)*1)
                        if(htsink_temp != self.controllerTemperature):
                            self.controllerTemperature = htsink_temp
                            vehicleReadings.controllerTemperature(self.controllerTemperature)

                        dig_input = int(int(dig_input_hex, 16)*1)

                        logMessage = 'Motor :' + str(message.arbitration_id) + ' : '+ 'Odometer Reading (NA): ' + str(self.odometer)
                        self.canLogger.warning(logMessage)
    
                    elif message.arbitration_id == 773:
                        data = message.data
                        new_data = [data[0], data[2], data[1], data[4], data[3], data[6], data[5], data[7]]
                        self.chargingCurrentCharger = round(((new_data[3]<<8) + new_data[4])*0.1, 2)
                        self.canLogger.warning(self.chargingCurrentCharger)
                    elif message.arbitration_id == 768:
                        data=message.data
                        #new_data = [data[0], data[2], data[1], data[4], data[3], data[6], data[5], data[7]]
                        self.canLogger.debug('Charging Command')

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
            publishSOC(self.stateOfCharge, self.rangeSuste, self.rangeThikka, self.rangeBabbal)
            #self.stateOfCharge = 55
            # print('SOC: ', self.stateOfCharge)
            # self.gpioWriter.setSOC(self.stateOfCharge)
            time.sleep(1)
    
    def logData(self):
        while True:
            message = str(self.stateOfCharge) + ' : ' + str(self.bikeSpeed) + ' : ' + str(self.motorCurrent) + ' : ' + str(self.motorVoltage) + ' : ' + str(self.actualTorque)  + ' : ' + str(self.odometer)
            self.dataLogger.info(message)
            # updateSpeed(self.bikeSpeed)
            time.sleep(0.1)

    def startCAN(self):
        self.tExtractCANData = threading.Thread(target=self.extractCANData)
        self.tExtractCANData.start()
        self.tRequestFrames = threading.Thread(target=self.requestCANFrames)
        # self.tRequestFrames.start()
        self.tPushFastData = threading.Thread(target=self.pushFastData)
        self.tPushFastData.start()
        self.tPushSlowData = threading.Thread(target=self.pushSlowData)
        self.tPushSlowData.start()
        self.tPrintData = threading.Thread(target=self.printData)
        #self.tPrintData.start()
        self.tLogData = threading.Thread(target = self.logData)
        self.tLogData.start()

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
    