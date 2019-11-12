import logging
import threading
import time
import can
import random
import os

class CANHandler:
    def __init__(self):
        #Parameters
        self.chargingStatus = 'Discharging'
        self.chargingCurrent        = 0     # Ampere
        self.packVoltage            = 0     # Volts
        self.stateOfCharge          = 0     # Percentage
        self.timeToCharge           = 0     # Minutes
        self.timeToDischarge        = 0     # Minutes
        self.highTemp               = 0     # Celsius      
        self.lowTemp                = 0     # Celsius
        self.bikeSpeed              = 0     # RPM
        self.maxTorque              = 0     # Newton-meter
        self.actualTorque           = 0     # Newton-meter
        self.motorTemp              = 0     # Celsius
        self.driveMode              = 0
        self.odometer               = 0     # km
        self.peakChargingCurrent    = 0     # Ampere
        self.peakDischargingCurrent  = 0     # Ampere
        self.dischargingCurrent     = 0     # Ampere

        #Configure CAN Interface
        can.rc['interface'] = 'socketcan_native'
        can.rc['channel'] = 'can0'
        self.bus = can.interface.Bus()

        #Configure logger
        logging.basicConfig(filename="can.log", format = '%(asctime)s - %(levelname)s - %(message)s', filemode='w')
        self.canLogger=logging.getLogger()
        self.canLogger.setLevel(logging.INFO)
        
        #Start CAN
        self.startCAN()

    def extractCANData(self):
        while True:
            message = self.bus.recv(0.1)
            if message is not None:
                if message.arbitration_id != 128:
                    if message.arbitration_id == 415236097:
                        data = message.data
                        #Battery Frame 0
                        if( (len(data) > 1) and (data[0] == 0)):
                            new_data=[data[0], data[2], data[1], data[4], data[3], data[6], data[5], data[7] ]

                            batteryStatus = (new_data[1]<<8) + new_data[2]
                            if((batteryStatus & 128) == 0):
                                self.chargingStatus = 'Discharging'
                            else:
                                self.chargingStatus = 'Charging'

                            self.packVoltage = round( ((new_data[3]<<8) + new_data[4])*0.1 , 1) 

                            self.chargingCurrent = round(((new_data[5]<<8) + new_data[6])*0.01, 1)
                            logMessage = 'Frame:    0' + ' - ' + 'ChargingCurrent: ' + str(self.chargingCurrent) + ' A ' + ' - ' + 'PackVoltage:    ' + str(self.packVoltage) + ' V' + ' - ' + 'ChargingStatus:  ' + str(self.chargingStatus)
                            #print(logMessage)
                            self.canLogger.info(logMessage)
                        
                        #Battery Frame 1   
                        # elif( (len(data) > 1) and (data[0] == 1)):
                        #     #print('Frame 1 Received')
                        #     new_data=[data[0], data[2], data[1], data[4], data[3], data[6], data[5], data[7] ]

                        #     self.peakChargingCurrent = round(((new_data[1]<<8) + new_data[2])*0.01, 1)
                        #     self.dischargingCurrent = round(((new_data[3]<<8) + new_data[4])*0.01, 1)
                        #     self.peakDischargingCurrent = round(((new_data[5]<<8) + new_data[6])*0.01, 1)
                        #     logMessage = 'Frame:    1' + ' - ' + 'PeakCC:    ' + str(self.peakChargingCurrent) + ' A' + ' - ' + 'DischargingCurrent:  ' + str(self.dischargingCurrent) + ' A' + ' - ' + 'PeakDC:  ' + str(self.peakDischargingCurrent) + ' A'
                        #     print(new_data)
                        #     print(logMessage)
                        #     self.canLogger.info(logMessage)
                        #Battery Frame 2
                        elif( (len(data) > 1) and (data[0] == 2)):
                            new_data=[data[0], data[2], data[1], data[3], data[4], data[6], data[5], data[7] ]

                            self.averageCurrent = round(((new_data[1]<<8) + new_data[2])*0.01, 1)

                            logMessage = 'Frame:    2' + ' - ' + 'AverageCurrent:    ' + str(self.averageCurrent) + ' A'
                            print(logMessage)
                            self.canLogger.info(logMessage)
                        
                        #Battery Frame 4   
                        elif( (len(data) > 1) and (data[0] == 4)):
                            new_data=[data[0], data[2], data[1], data[3], data[4], data[6], data[5], data[7] ]

                            self.highTemp = round(((new_data[1]<<8) + new_data[2])*0.1, 1)

                            self.lowTemp = round(((new_data[5]<<8) + new_data[6])*0.1, 1)
                            logMessage = 'Frame:    4' + ' - ' + 'HighTemp:    ' + str(self.highTemp) + ' Celsius' + ' - ' + 'LowTemp:  ' + str(self.lowTemp) + ' Celsius'
                            #print(logMessage)
                            self.canLogger.info(logMessage)
                        
                        #Battery Frame 5
                        elif( (len(data) > 1) and (data[0] == 5)):
                            new_data=[data[0], data[1], data[3], data[2], data[5], data[4], data[7], data[6] ]
                            self.stateOfCharge = round(((new_data[2]<<8) + new_data[3])*0.1 , 1)

                            self.timeToCharge = (new_data[6]<<8) + new_data[7]
                            logMessage = 'Frame:    5' + ' - ' + 'SOC:  ' + str(self.stateOfCharge) + ' % - TimeToCharge:   ' + str(self.timeToCharge) + ' min '
                            #print(logMessage)
                            self.canLogger.info(logMessage)
                        #Battery Frame 6
                        elif( (len(data) > 1) and (data[0] == 6)):
                            new_data=[data[0], data[2], data[1], data[4], data[3], data[6], data[5], data[7] ]

                            self.timeToDischarge = round(((new_data[1]<<8) + new_data[2]), 1)
                            logMessage = 'Frame:    6' + ' - ' + 'TimeToDischarge:    ' + str(self.highTemp) + ' Celsius'
                            #print(logMessage)
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
                        print('Battery Current from Motor: ', bat_current)
                        bat_voltage = int(int(bat_voltage_hex, 16)*0.0625)
                        bat_v_notint = int(bat_voltage_hex, 16)*0.0625
                        # Fix negative current issue
                        if bat_current > 4096/2:
                            bat_current = int(bat_current - 4096)
                            recuperation = 1
                        else:
                            recuperation = 0
                        # Calculate Battery SoC and Range
                        s_o_charge = int((bat_v_notint - 95.12) / (101.2 - 95.12) * 100)
                        if s_o_charge < 0:
                            s_o_charge = 0
                        elif s_o_charge > 100:
                            s_o_charge = 100
                        est_range = s_o_charge * 1.5  # Assuming 150km when 100%
                    # Motor Controller
                    elif message.arbitration_id == 1024:
                        # Perform data swap in binary
                        data = message.data
                        new_data = [data[1], data[0], data[3], data[2], data[5], data[4], data[7], data[6]]
                        self.bikeSpeed = round(((new_data[0]<<8) + new_data[1])*0.0625, 1)
                        self.maxTorque = round(((new_data[2]<<8) + new_data[3])*0.1, 1)
                        self.actualTorque = round(((new_data[4]<<8) + new_data[5])*0.0625, 1)
                        self.motorTemp = round(((new_data[6]<<8) + new_data[7]), 1)
                        # Fix negative velocity issue
                        if self.bikeSpeed > 4096/2:
                            self.bikeSpeed = 0
                        # Fix negative torque issue
                        if self.actualTorque > 4096/2:
                            self.actualTorque = int(self.actualTorque-4096)
                        logMessage = 'Frame:    1024' + ' - ' + 'BikeSpeed:  ' + str(self.bikeSpeed) + ' rpm - ActualTorque:   ' + str(self.actualTorque) + ' Nm '
                        #print(logMessage)
                        self.canLogger.info(logMessage)
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
                        logMessage = 'Frame:    664' + ' - ' + 'DriveMode:  ' + str(drive_prof)
                        #print(logMessage)
                        self.canLogger.info(logMessage)
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
                        htsink_temp = int(int(htsink_temp_hex, 16)*1)
                        dig_input = int(int(dig_input_hex, 16)*1)
                        logMessage = 'Frame:    769' + ' - ' + 'Odometer:  ' + str(odometer) + ' km'
                        #print(logMessage)
                        self.canLogger.info(logMessage)

    def requestCANFrames(self):
        while True:
            frame = can.Message(arbitration_id=0x18C00001,data=[0], extended_id=True)
            self.bus.send(frame)
            time.sleep(0.1)
            frame = can.Message(arbitration_id=0x18C00001,data=[2], extended_id=True)
            self.bus.send(frame)
            #print('Frame 1 Requested')
            time.sleep(0.1)
            frame = can.Message(arbitration_id=0x18C00001,data=[4], extended_id=True)
            self.bus.send(frame)
            time.sleep(0.1)
            frame = can.Message(arbitration_id=0x18C00001,data=[5], extended_id=True)
            self.bus.send(frame)
            time.sleep(0.1)
            frame = can.Message(arbitration_id=0x18C00001,data=[6], extended_id=True)
            self.bus.send(frame)
            time.sleep(0.5)

    
    def startCAN(self):
        self.tExtractCANData = threading.Thread(target=self.extractCANData)
        self.tExtractCANData.start()
        self.tRequestFrames = threading.Thread(target=self.requestCANFrames)
        self.tRequestFrames.start()
        # self.tPrintData = threading.Thread(target=self.printData)
        # self.tPrintData.start()

    def printData(self):
        while True:
            time.sleep(0.5)
            os.system('clear')
            print('Drive Mode                   : ', self.driveMode)
            print('Bike Speed                   : ', self.bikeSpeed, '      kmph')
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