import json
from periphery import GPIO
import vehicle_states

class GPIOManager():

    """
    __init__:
        initializes the variables/states
        intializes the GPIOs
    """
    def __init__(self, gpio_config_file):
        self.pinState = {
                        eGPIO.IN_HIBEAM:0,
                        eGPIO.IN_LTURN:0,
                        eGPIO.IN_RTURN:0,
                        eGPIO.IN_BUTTON_RD:0,
                        eGPIO.IN_BUTTON_RU:0,
                        eGPIO.IN_BUTTON_RB:0,
                        eGPIO.IN_STAND:0
                    }
        self.initializeGPIO(gpio_config_file)

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
        
        self.out_start_thikka = GPIO(config['out_start_thikka']['pin'], config['out_start_thikka']['direction'])
        self.out_suste = GPIO(config['out_suste']['pin'], config['out_suste']['direction'])
        self.out_reverse = GPIO(config['out_reverse']['pin'], config['out_reverse']['direction'])
        self.out_babbal = GPIO(config['out_babbal']['pin'], config['out_babbal']['direction'])
        self.out_charge = GPIO(config['out_charge']['pin'], config['out_charge']['direction'])
        self.out_ign = GPIO(config['out_ign']['pin'], config['out_ign']['direction'])
        self.out_lturn = GPIO(config['out_lturn']['pin'], config['out_lturn']['direction'])
        self.out_rturn = GPIO(config['out_rturn']['pin'], config['out_rturn']['direction'])

    """
    monitorPins:
        reads the state of the pins
        updates the pin_state member variable
    """
    def monitorGPIO(self):
        inputState[eGPIO.IN_HIBEAM] = in_hibeam.read()
        inputState[eGPIO.IN_LTURN] = in_lturn.read()
        inputState[eGPIO.IN_RTURN] = in_rturn.read()
        inputState[eGPIO.IN_BUTTON_RD] = in_button_rb.read()
        inputState[eGPIO.IN_BUTTON_RU] = in_button_rb.read()
        inputState[eGPIO.IN_BUTTON_RB] = in_button_rb.read()
        inputState[eGPIO.IN_STAND] = in_stand.read()
        
        inputChanges = self.determineInputChange(inputState)
        self.pinState = inputState
        return inputChanges, inputState
    """
    determineInputChange:
        finds out if the state has changed
    """
    def determineInputChange(self, inputState):
        inputChanges = []
        for pin in inputState:
            if inputState[pin] != self.pinState[pin]:
                inputChanges.append(pin)
        return inputChanges