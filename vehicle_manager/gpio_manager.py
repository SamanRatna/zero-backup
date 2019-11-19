import json
import RPi.GPIO as GPIO
from vehicle_states import *
from event_handler import *
import threading
from time import sleep
from time import time

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
        GPIO.add_event_detect(2, GPIO.FALLING, callback=self.threadHibeam , bouncetime=250)
        GPIO.add_event_detect(10, GPIO.FALLING, callback=self.threadStand ,bouncetime=250)
        # GPIO.add_event_detect(9, GPIO.FALLING, callback=threadBrake ,bouncetime=150)
        GPIO.add_event_detect(3, GPIO.FALLING, callback=self.threadLeftTurn ,bouncetime=250)
        GPIO.add_event_detect(4, GPIO.FALLING, callback=self.threadRightTurn ,bouncetime=250)
        GPIO.add_event_detect(27, GPIO.FALLING, callback=self.threadRUPress ,bouncetime=250)
        # GPIO.add_event_detect(22, GPIO.FALLING, callback=self.threadRBPress ,bouncetime=250)
        # GPIO.add_event_detect(17, GPIO.FALLING, callback=threadRDPress ,bouncetime=150)

    def initializeGPIOThreads(self):
        # self.tHibeam = threading.Thread(target = self.threadHibeam)
        # self.tStand = threading.Thread(target = self.threadStand)
        self.tBrake = threading.Thread(target = self.threadBrake)
        # self.tLTurn = threading.Thread(target = self.threadLeftTurn)
        # self.tRTurn = threading.Thread(target = self.threadRightTurn)
        self.tRUPress = threading.Thread(target = self.threadRUPress)
        self.tRBPress = threading.Thread(target = self.threadRBPress)
        self.tRDPress = threading.Thread(target = self.threadRDPress)
        # self.tLowBattery = threading.Thread(target = self.threadLowBattery)
        # self.tHibeam.start()
        # self.tStand.start()
        self.tBrake.start()
        # self.tLTurn.start()
        # self.tRTurn.start()
        self.tRUPress.start()
        self.tRBPress.start()
        self.tRDPress.start()
    def threadLowBattery(self):
        while True:
            GPIO.output(19, False)
            GPIO.output(26, False)  
            sleep(0.5)
            GPIO.output(19, True)
            GPIO.output(26, True)
            sleep(0.5)

    def threadHibeam(self, value):
            state = GPIO.input(2);
            vehicleEvents.onHibeamToggle(state)

    def threadLeftTurn(self, value):
            vehicleEvents.onLeftSideLightToggle()

    def threadRightTurn(self, value):
            vehicleEvents.onRightSideLightToggle()
    
    def threadRBPress(self):
        while True:
            sleep(0.2)
            state = GPIO.input(22)
            #print('RB state: ', state)
            if( state == GPIO.LOW):
                vehicleEvents.onRBPress()

    def threadRDPress(self):
        while True:
            GPIO.wait_for_edge(17, GPIO.FALLING)
            button_press = time()
            sleep(0.2)
            #GPIO.wait_for_edge(17, GPIO.RISING)
            while GPIO.input(17) == GPIO.LOW:
                sleep(0.01)
            button_release = time()
            print(button_release - button_press)
            if ((button_release - button_press) < 0.8):
                vehicleEvents.onRDPress()
            else:
                vehicleEvents.onRDHold()
            sleep(0.2)

    def threadRUPress(self):
        while True:
            sleep(0.2)
            state = GPIO.input(27)
            #print('RU state: ', state)
            if( state == GPIO.LOW):
                vehicleEvents.onRUPress()
    def threadStand(self, value):
            state = GPIO.input(pin)
            vehicleEvents.onStandSwitch(state)
    
    def threadBrake(self):
        state_0 = GPIO.input(9)
        while True:
            state_1 = GPIO.input(9)
            if (state_0 != state_1):
                #print("Brake State: "+ str(state_1))
                vehicleEvents.onBrakeToggle(state_1)
                state_0 = state_1
            sleep(0.2)

    def monitorGPIO(self):
        inputState= {}
        inputState[eGPIO.IN_HIBEAM] = self.in_hibeam.read()
        inputState[eGPIO.IN_LTURN] = self.in_lturn.read()
        inputState[eGPIO.IN_RTURN] = self.in_rturn.read()
        inputState[eGPIO.IN_BUTTON_RD] = self.in_button_rd.read()
        inputState[eGPIO.IN_BUTTON_RU] = self.in_button_ru.read()
        inputState[eGPIO.IN_BUTTON_RB] = self.in_button_rb.read()
        inputState[eGPIO.IN_STAND] = self.in_stand.read()
        self.inputState = inputState

    def updateGPIO(self):
        self.monitorGPIO()
        self.processInput()
        self.pinState = self.inputState

    def processInput(self):
        for pin in self.inputState:
            if self.inputState[pin] != self.pinState[pin]:
                self.invokeEvent(pin, self.inputState[pin])
    
    def primeInput(self):
        self.monitorGPIO()
        self.invokeEvent(eGPIO.IN_HIBEAM, self.inputState[eGPIO.IN_HIBEAM])
        self.invokeEvent(eGPIO.IN_STAND, self.inputState[eGPIO.IN_STAND])
        self.pinState = self.inputState

    def invokeEvent(self, eventId, value):
        if eventId == eGPIO.IN_HIBEAM:
            vehicleEvents.onHibeamToggle(value)
        elif eventId == eGPIO.IN_LTURN:
            vehicleEvents.onLeftSideLightToggle()
        elif eventId == eGPIO.IN_RTURN:
            vehicleEvents.onRightSideLightToggle()
        elif eventId == eGPIO.IN_BUTTON_RB:
            vehicleEvents.onRBPress()
        elif eventId == eGPIO.IN_BUTTON_RD:
            vehicleEvents.onRDPress()
        elif eventId == eGPIO.IN_BUTTON_RU:
            vehicleEvents.onRUPress()
        elif eventId == eGPIO.IN_STAND:
            vehicleEvents.onStandSwitch(value)

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
        self.bootupLedAnimation()

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
        


class GPIOWriterMock:
    def __init__(self):
        print('Mocking GPIOWriter')
