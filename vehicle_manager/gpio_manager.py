import json
from periphery import GPIO
from vehicle_states import *
from event_handler import *
import threading

class GPIOReader():
    __instance = None
    @staticmethod
    def getInstance():
        if GPIOReader.__instance == None:
            GPIOReader()
        return GPIOReader.__instance

    """
    __init__:
        initializes the variables/states
        intializes the GPIOs
    """
    def __init__(self):
        if GPIOReader.__instance != None:
            raise Exception("GPIOReader is a Singleton Class.")
        else:
            GPIOReader.__instance = self
            self.initializeGPIO('gpio_config.json')
            self.initializeGPIOThreads()
            self.primeInput()
            self.startGPIOThreads()
            
    """
    initializeGPIO:
        initializes the GPIOs with the help of config file provided as an argument
    """
    def initializeGPIO(self, gpio_config_file):
        with open(gpio_config_file) as cfg_file:
            config = json.load(cfg_file)

        self.in_hibeam = GPIO(config['in_hibeam']['pin'], config['in_hibeam']['direction'])
        self.in_hibeam.edge = "both"

        self.in_lturn = GPIO(config['in_lturn']['pin'], config['in_lturn']['direction'])
        self.in_lturn.edge = "falling"

        self.in_rturn = GPIO(config['in_rturn']['pin'], config['in_rturn']['direction'])
        self.in_rturn.edge = "falling"

        self.in_button_rd = GPIO(config['in_button_rd']['pin'], config['in_button_rd']['direction'])
        self.in_button_rd.edge = "falling"

        self.in_button_ru = GPIO(config['in_button_ru']['pin'], config['in_button_ru']['direction'])
        self.in_button_ru.edge = "falling"

        self.in_button_rb = GPIO(config['in_button_rb']['pin'], config['in_button_rb']['direction'])
        self.in_button_rb.edge = "falling"

        self.in_stand = GPIO(config['in_stand']['pin'], config['in_stand']['direction'])
        self.in_stand.edge = "both"

        self.in_brake = GPIO(config['in_brake']['pin'], config['in_brake']['direction'])
        self.in_brake.edge = "both"

    def initializeGPIOThreads(self):
        self.tHibeam = threading.Thread(target = self.threadHibeam)
        self.tStand = threading.Thread(target = self.threadStand)
        self.tBrake = threading.Thread(target = self.threadBrake)
        self.tLTurn = threading.Thread(target = self.threadLeftTurn)
        self.tRTurn = threading.Thread(target = self.threadRightTurn)
        self.tRUPress = threading.Thread(target = self.threadRUPress)
        self.tRBPress = threading.Thread(target = self.threadRBPress)
        self.tRDPress = threading.Thread(target = self.threadRDPress)

    def startGPIOThreads(self):
        self.tHibeam.start()
        self.tStand.start()
        self.tBrake.start()
        self.tLTurn.start()
        self.tRTurn.start()
        self.tRUPress.start()
        self.tRBPress.start()
        self.tRDPress.start()
    
    def primeInput(self):
        beamState = self.in_hibeam.read()
        standState = self.in_stand.read()
        brakeState = self.in_brake.read()
        vehicleEvents.onBrakeToggle(brakeState)
        vehicleEvents.onHibeamToggle(beamState)
        vehicleEvents.onStandSwitch(standState)

    def threadHibeam(self):
        while True:
            self.in_hibeam.poll()
            state = self.in_hibeam.read()
            vehicleEvents.onHibeamToggle(state)
    
    def threadLeftTurn(self):
        while True:
            state = self.in_lturn.poll()
            vehicleEvents.onLeftSideLightToggle(state)
    
    def threadRightTurn(self):
        while True:
            state = self.in_rturn.poll()
            vehicleEvents.onRightSideLightToggle(state)
    
    def threadRBPress(self):
        while True:
            state = self.in_button_rb.poll()
            vehicleEvents.onRBPress()

    def threadRDPress(self):
        while True:
            state = self.in_button_rd.poll()
            vehicleEvents.onRDPress()

    def threadRUPress(self):
        while True:
            state = self.in_button_ru.poll()
            vehicleEvents.onRUPress()

    def threadStand(self):
        while True:
            self.in_stand.poll()
            state = self.in_stand.read()
            vehicleEvents.onStandSwitch()
    
    def threadBrake(self):
        while True:
            self.in_brake.poll()
            state = self.in_brake.read()
            vehicleEvents.onBrakeToggle(state)

class GPIOWriter():
    __instance = None
    @staticmethod
    def getInstance():
        if GPIOWriter.__instance == None:
            GPIOWriter()
        return GPIOWriter.__instance
    """
    __init__:
        initializes the variables/states
        intializes the GPIOs
    """
    def __init__(self):
        if GPIOWriter.__instance != None:
            raise Exception("GPIOWriter is a Singleton Class.")
        else:
            GPIOWriter.__instance = self
            self.initializeGPIO('gpio_config.json')
    """
    initializeGPIO:
        initializes the GPIOs with the help of config file provided as an argument
    """
    def initializeGPIO(self, gpio_config_file):
        with open(gpio_config_file) as cfg_file:
            config = json.load(cfg_file)
        
        self.out_start_thikka = GPIO(config['out_start_thikka']['pin'], config['out_start_thikka']['direction'])
        self.out_suste = GPIO(config['out_suste']['pin'], config['out_suste']['direction'])
        self.out_reverse = GPIO(config['out_reverse']['pin'], config['out_reverse']['direction'])
        self.out_babbal = GPIO(config['out_babbal']['pin'], config['out_babbal']['direction'])
        self.out_charge = GPIO(config['out_charge']['pin'], config['out_charge']['direction'])
        self.out_charge_motor = GPIO(config['out_charge_motor']['pin'], config['out_charge_motor']['direction'])
        self.out_ign = GPIO(config['out_ign']['pin'], config['out_ign']['direction'])
        self.out_lturn = GPIO(config['out_lturn']['pin'], config['out_lturn']['direction'])
        self.out_rturn = GPIO(config['out_rturn']['pin'], config['out_rturn']['direction'])
        self.out_brake = GPIO(config['out_brake']['pin'], config['out_brake']['direction'])

    def setIgn(self, value):
        self.out_ign.write(value)
    
    def setLTurn(self, value):
        self.out_lturn.write(value)
    
    def setRTurn(self, value):
        self.out_rturn.write(value)
    
    def setCharge(self, value):
        self.out_charge.write(value)

    def setBrake(self, value):
        self.out_brake.write(value)

    def setMode(self, mode):
        if mode == eBikeMode.MODE_THIKKA:
            self.out_suste.write(True)
            self.out_babbal.write(True)
            self.out_reverse.write(True)
            self.out_charge_motor.write(True)
            self.out_start_thikka.write(False)

        elif mode == eBikeMode.MODE_SUSTE:
            self.out_babbal.write(True)
            self.out_reverse.write(True)
            self.out_start_thikka.write(True)
            self.out_charge_motor.write(True)
            self.out_suste.write(False)

        elif mode == eBikeMode.MODE_BABBAL:
            self.out_reverse.write(True)
            self.out_start_thikka.write(True)
            self.out_suste.write(True)
            self.out_charge_motor.write(True)
            self.out_babbal.write(False)
        elif mode == eBikeMode.MODE_REVERSE:
            self.out_start_thikka.write(True)
            self.out_suste.write(True)
            self.out_babbal.write(True)
            self.out_charge_motor.write(True)
            self.out_reverse.write(False)

        elif mode == eBikeMode.MODE_CHARGING:
            self.out_start_thikka.write(True)
            self.out_suste.write(True)
            self.out_babbal.write(True)
            self.out_reverse.write(True)
            self.out_charge_motor.write(False)

        elif mode == eBikeMode.MODE_STANDBY:
            self.out_start_thikka.write(True)
            self.out_suste.write(True)
            self.out_babbal.write(True)
            self.out_reverse.write(True)
            self.out_charge_motor.write(True)
