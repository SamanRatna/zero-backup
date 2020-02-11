import json
import RPi.GPIO as GPIO
from vehicle_states import *
from event_handler import *
import threading
from time import sleep
from time import time
import pin
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
            self.pinState = {}
            self.inputState = {}
            self.rdTimer = RepeatableTimer(1.0, self.rdBtnProcess)
            self.btnDown = 0
            self.btnUp = 0
            self.initializeGPIO()
            self.initializeGPIOThreads()

    """
    initializeGPIO:
        initializes the GPIOs with the help of config file provided as an argument
    """
    def initializeGPIO(self):
        GPIO.setmode(GPIO.BCM)
        inputChannel = [2,3,4,17,27,22,10,9]
        GPIO.setup(inputChannel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    def rdBtnProcess(self):
        vehicleEvents.onRDHold()
    def initializeGPIOThreads(self):
        self.tRDPress = threading.Thread(target = self.threadRDPress)
        self.tRDPress.start()
   
    def threadRDPress(self):
        self.monitorGPIO()
        self.pinState = self.inputState
        while True:
            self.monitorGPIO()
            self.processInput()
            self.pinState = self.inputState
            sleep(0.1)

    def monitorGPIO(self):
        inputState= {}
        inputState[eGPIO.IN_HIBEAM] = GPIO.input(pin.IN_HIBEAM)
        inputState[eGPIO.IN_LTURN] = GPIO.input(pin.IN_LTURN)
        inputState[eGPIO.IN_RTURN] = GPIO.input(pin.IN_RTURN)
        inputState[eGPIO.IN_BUTTON_RD] = GPIO.input(pin.IN_BTN_RD)
        inputState[eGPIO.IN_BUTTON_RU] = GPIO.input(pin.IN_BTN_RU)
        inputState[eGPIO.IN_BUTTON_RB] = GPIO.input(pin.IN_BTN_RB)
        inputState[eGPIO.IN_STAND] = GPIO.input(pin.IN_STAND)
        inputState[eGPIO.IN_BRAKE] = GPIO.input(pin.IN_BRAKE)
        self.inputState = inputState

    def updateGPIO(self):
        while True:
            self.monitorGPIO()
            self.processInput()
            self.pinState = self.inputState
            sleep(0.1)

    def processInput(self):
        for x in self.inputState:
            if self.inputState[x] != self.pinState[x]:
                self.invokeEvent(x, self.inputState[x])
    
    def primeInput(self):
        self.monitorGPIO()
        self.invokeEvent(eGPIO.IN_HIBEAM, self.inputState[eGPIO.IN_HIBEAM])
        self.invokeEvent(eGPIO.IN_STAND, self.inputState[eGPIO.IN_STAND])
        self.pinState = self.inputState

    def invokeEvent(self, eventId, value):
        if eventId == eGPIO.IN_HIBEAM:
            vehicleEvents.onHibeamToggle(value)
        elif eventId == eGPIO.IN_LTURN:
            if value == False:   
                vehicleEvents.onLeftSideLightToggle(value)
        elif eventId == eGPIO.IN_RTURN:
            if value == False:
                vehicleEvents.onRightSideLightToggle(value)
        elif eventId == eGPIO.IN_BUTTON_RB:
            if value == False:
                vehicleEvents.onRBPress()
        elif eventId == eGPIO.IN_BUTTON_RD:
            # if value == False:
            #     self.btnDown = time()
            # elif value == True:
            #     self.btnUp = time()
            #     if(self.btnUp - self.btnDown < 0.5):
            #         vehicleEvents.onRDPress()
            #     else:
            #         vehicleEvents.onRDHold()
            if value == False:
                self.rdTimer.start()
            else:
                if self.rdTimer.isAlive():
                    self.rdTimer.cancel()
                    vehicleEvents.onRDPress()

        elif eventId == eGPIO.IN_BUTTON_RU:
            if value == False:
                vehicleEvents.onRUPress()
        elif eventId == eGPIO.IN_STAND:
            vehicleEvents.onStandSwitch(value)
        elif eventId == eGPIO.IN_BRAKE:
            vehicleEvents.onBrakeToggle(value)

class RepeatableTimer(object):
    def __init__(self, interval, function, args=[], kwargs={}):
        self._interval = interval
        self._function = function
        self._args = args
        self._kwargs = kwargs
        self.t = threading.Timer(self._interval, self._function, *self._args, **self._kwargs)
    def start(self):
        self.t = threading.Timer(self._interval, self._function, *self._args, **self._kwargs)
        self.t.start()
    def cancel(self):
        print('Cancelling the timer.')
        self.t.cancel()
    def isAlive(self):
        print('Timer is Alive.')
        return self.t.is_alive()
        
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
            self.initializeGPIO()
    """
    initializeGPIO:
        initializes the GPIOs with the help of config file provided as an argument
    """
    def initializeGPIO(self):
        GPIO.setmode(GPIO.BCM)
        outputChannel = [14, 15, 18, 23, 24, 25, 8, 7, 16, 12]
        ledChannel = [5, 6, 13, 19, 26]
        GPIO.setup(outputChannel, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(ledChannel, GPIO.OUT, initial=GPIO.LOW)
        # self.bootupLedAnimation()

    def setIgn(self, value):
        GPIO.output(8, value)
    
    def setLTurn(self, value):
        GPIO.output(7, value)
    
    def setRTurn(self, value):
        GPIO.output(16, value)
    
    def setCharge(self, value):
        GPIO.output(25, value)
    
    def setBrake(self, value):
        GPIO.output(12, value)

    def setMode(self, mode):
        if mode == eBikeMode.MODE_THIKKA:
            GPIO.output(14, True)
            GPIO.output(18, True)
            GPIO.output(23, True)
            GPIO.output(25, True)
            GPIO.output(15, False)
            #led-output
            GPIO.output(5, False)
            GPIO.output(6, True)
            GPIO.output(13, False)

        elif mode == eBikeMode.MODE_SUSTE:
            GPIO.output(18, True)
            GPIO.output(23, True)
            GPIO.output(15, False)
            GPIO.output(24, True)
            GPIO.output(14, False)
            #led-output
            GPIO.output(5, True)
            GPIO.output(6, False)
            GPIO.output(13, False)

        elif mode == eBikeMode.MODE_BABBAL:
            GPIO.output(23, True)
            GPIO.output(15, False)
            GPIO.output(24, True)
            GPIO.output(14, True)
            GPIO.output(18, False)
            #led-output
            GPIO.output(5, False)
            GPIO.output(6, False)
            GPIO.output(13, True)

        elif mode == eBikeMode.MODE_REVERSE:
            GPIO.output(15, True)
            GPIO.output(24, True)
            GPIO.output(14, True)
            GPIO.output(18, True)
            GPIO.output(23, False)
            #led-output
            GPIO.output(5, False)
            GPIO.output(6, False)
            GPIO.output(13, False)

        elif mode == eBikeMode.MODE_CHARGING:
            GPIO.output(15, True)
            GPIO.output(14, True)
            GPIO.output(18, True)
            GPIO.output(23, True)
            GPIO.output(24, False)
            #led-output
            GPIO.output(5, True)
            GPIO.output(6, False)
            GPIO.output(13, True)

        elif mode == eBikeMode.MODE_STANDBY:
            GPIO.output(15, True)
            GPIO.output(14, True)
            GPIO.output(18, True)
            GPIO.output(23, True)
            GPIO.output(24, False)
            #led-output
            #self.bootupLedAnimation()
            

            GPIO.output(5, True)
            GPIO.output(6, True)
            GPIO.output(13, True)
    
    def setSOC(self, soc):
        if(soc >= 80):
            GPIO.output(19, True)
            GPIO.output(26, True)
        elif(soc >= 60):
            GPIO.output(19, True)
            GPIO.output(26, False)        
        elif(soc >= 40):
            GPIO.output(19, False)
            GPIO.output(26, True)        
        elif(soc >= 20):
            GPIO.output(19, False)
            GPIO.output(26, False)  
            sleep(0.3)
            GPIO.output(19, True)
            GPIO.output(26, True)
            sleep(0.3)      
        else:
            GPIO.output(19, False)
            GPIO.output(26, False)  

    def bootupLedAnimation(self):
        GPIO.output(5,True)
        sleep(0.2)
        GPIO.output(5,False)
        GPIO.output(6,True)
        sleep(0.2)
        GPIO.output(6,False)
        GPIO.output(13,True)
        sleep(0.2)
        GPIO.output(13,False)
        GPIO.output(19,True)
        sleep(0.2)
        GPIO.output(19,False)
        GPIO.output(26,True)
        sleep(0.2)
        GPIO.output(26,False)
        sleep(0.2)
        GPIO.output(5,True)
        sleep(0.2)
        GPIO.output(5,False)
        GPIO.output(6,True)
        sleep(0.2)
        GPIO.output(6,False)
        GPIO.output(13,True)
        sleep(0.2)
        GPIO.output(13,False)
        GPIO.output(19,True)
        sleep(0.2)
        GPIO.output(19,False)
        GPIO.output(26,True)
        sleep(0.2)
        GPIO.output(26,False)
        sleep(0.2)

        GPIO.output(5,True)
        GPIO.output(6,True)
        GPIO.output(13,True)
        GPIO.output(19,True)
        GPIO.output(26,True)
        sleep(0.2)
        GPIO.output(5,False)
        GPIO.output(6,False)
        GPIO.output(13,False)
        GPIO.output(19,False)
        GPIO.output(26,False)
        sleep(0.2)
        GPIO.output(5,True)
        GPIO.output(6,True)
        GPIO.output(13,True)
        GPIO.output(19,True)
        GPIO.output(26,True)
        sleep(0.2)
        GPIO.output(5,False)
        GPIO.output(6,False)
        GPIO.output(13,False)
        GPIO.output(19,False)
        GPIO.output(26,False)
        sleep(0.2)
        GPIO.output(5,True)
        GPIO.output(6,True)
        GPIO.output(13,True)
        GPIO.output(19,True)
        GPIO.output(26,True)
        sleep(0.2)
        GPIO.output(5,False)
        GPIO.output(6,False)
        GPIO.output(13,False)
        GPIO.output(19,False)
        GPIO.output(26,False)

