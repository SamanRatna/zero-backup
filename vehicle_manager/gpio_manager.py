import json
from periphery import GPIO
from vehicle_states import *
from event_handler import *

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
            self.pinState = {
                            eGPIO.IN_HIBEAM:0,
                            eGPIO.IN_LTURN:0,
                            eGPIO.IN_RTURN:0,
                            eGPIO.IN_BUTTON_RD:0,
                            eGPIO.IN_BUTTON_RU:0,
                            eGPIO.IN_BUTTON_RB:0,
                            eGPIO.IN_STAND:0
                        }
            self.inputState = {
                            eGPIO.IN_HIBEAM:0,
                            eGPIO.IN_LTURN:0,
                            eGPIO.IN_RTURN:0,
                            eGPIO.IN_BUTTON_RD:0,
                            eGPIO.IN_BUTTON_RU:0,
                            eGPIO.IN_BUTTON_RB:0,
                            eGPIO.IN_STAND:0
                        }
            self.initializeGPIO('gpio_config.json')

    """
    initializeGPIO:
        initializes the GPIOs with the help of config file provided as an argument
    """
    def initializeGPIO(self, gpio_config_file):
        with open(gpio_config_file) as cfg_file:
            config = json.load(cfg_file)

        self.in_hibeam = GPIO(config['in_hibeam']['pin'], config['in_hibeam']['direction'])
        self.in_lturn = GPIO(config['in_lturn']['pin'], config['in_lturn']['direction'])
        self.in_rturn = GPIO(config['in_rturn']['pin'], config['in_rturn']['direction'])
        self.in_button_rd = GPIO(config['in_button_rd']['pin'], config['in_button_rd']['direction'])
        self.in_button_ru = GPIO(config['in_button_ru']['pin'], config['in_button_ru']['direction'])
        self.in_button_rb = GPIO(config['in_button_rb']['pin'], config['in_button_rb']['direction'])
        self.in_stand = GPIO(config['in_stand']['pin'], config['in_stand']['direction'])

    def monitorGPIO(self):
        self.inputState[eGPIO.IN_HIBEAM] = self.in_hibeam.read()
        self.inputState[eGPIO.IN_LTURN] = self.in_lturn.read()
        self.inputState[eGPIO.IN_RTURN] = self.in_rturn.read()
        self.inputState[eGPIO.IN_BUTTON_RD] = self.in_button_rd.read()
        self.inputState[eGPIO.IN_BUTTON_RU] = self.in_button_ru.read()
        self.inputState[eGPIO.IN_BUTTON_RB] = self.in_button_rb.read()
        self.inputState[eGPIO.IN_STAND] = self.in_stand.read()

        self.processInput(self.inputState)
        self.pinState = self.inputState

    def processInput(self, inputState):
        inputChanges = []
        for pin in inputState:
            if inputState[pin] != self.pinState[pin]:
                self.invokeEvent(pin, inputState[pin])

    def invokeEvent(self, eventId, value):
        if eventId == eGPIO.IN_HIBEAM:
            vehicleEvents.onHibeamToggle(value)
        elif eventId == eGPIO.IN_LTURN:
            vehicleEvents.onLeftSideLightToggle(value)
        elif eventId == eGPIO.IN_RTURN:
            vehicleEvents.onRightSideLightToggle(value)
        elif eventId == eGPIO.IN_BUTTON_RB:
            vehicleEvents.onRBPress()
        elif eventId == eGPIO.IN_BUTTON_RD:
            vehicleEvents.onRDPress()
        elif eventId == eGPIO.IN_BUTTON_RU:
            vehicleEvents.onRUPress()
        elif eventId == eGPIO.IN_STAND:
            vehicleEvents.onStandSwitch()

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
            #self.initializeGPIO('gpio_config.json')
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
        self.out_ign = GPIO(config['out_ign']['pin'], config['out_ign']['direction'])
        self.out_lturn = GPIO(config['out_lturn']['pin'], config['out_lturn']['direction'])
        self.out_rturn = GPIO(config['out_rturn']['pin'], config['out_rturn']['direction'])

class GPIOWriterMock:
    def __init__(self):
        print('Mocking GPIOWriter')