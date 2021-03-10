import signal
import RPi.GPIO as GPIO
from vehicle_states import *
from event_handler import *
import threading
from time import sleep
from time import time
import pin

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    GPIO.cleanup()
    exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

class RepeatableTimer(object):
    def __init__(self, interval, function, args=[], kwargs={}):
        self._interval = interval
        self._function = function
        self._args = args
        self._kwargs = kwargs
        self.t = threading.Timer(self._interval, self._function, *self._args, **self._kwargs)
    def start(self):
        self.t = threading.Timer(self._interval, self._function, *self._args, **self._kwargs)
        print('Starting the timer.')
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
        outputChannel = [pin.OUT_BRIGHT_MINUS, pin.OUT_BRIGHT_PLUS, pin.OUT_DISPLAY]
        GPIO.setup(outputChannel, GPIO.OUT, initial=GPIO.HIGH)
        vehicleEvents.onBrightnessChange += self.setBrightness

    def setBrightness(self, brightness):
        if(brightness == 1):
            GPIO.output(pin.OUT_BRIGHT_PLUS, False)
            sleep(0.15)
            GPIO.output(pin.OUT_BRIGHT_PLUS, True)
        elif(brightness == -1):
            GPIO.output(pin.OUT_BRIGHT_MINUS, False)
            sleep(0.15)
            GPIO.output(pin.OUT_BRIGHT_MINUS, True)
        print('Brightness Delta: ', brightness)

    def onBikeOff(self):
        print('Turning OFF the display.')
        GPIO.output(pin.OUT_DISPLAY, False)
        sleep(0.15)
        GPIO.output(pin.OUT_DISPLAY, True)

    def onBikeOn(self):
        print('Turning ON the display.')
        GPIO.output(pin.OUT_DISPLAY, False)
        sleep(0.15)
        GPIO.output(pin.OUT_DISPLAY, True)
