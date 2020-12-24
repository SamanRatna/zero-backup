from event_handler import *
import threading
from gpio_manager import RepeatableTimer
import subprocess

class PowerManager():
    def __init__(self):
        self.standState = 0
        vehicleEvents.onStandSwitch += self.updateStandState
        vehicleEvents.onUserInteraction += self.uiMonitor
        vehicleEvents.bikeOff += self.onBikeOff
        vehicleEvents.bikeOn += self.onBikeOn
        # self.inactivityTimer = threading.Timer(5.0, self.poweroff)
        self.inactivityTimer = RepeatableTimer(10.0, self.poweroff)
    def updateStandState(self, state):
        self.standState = state
        self.standMonitor(state)
    
    def poweroff(self):
        print('User inactive.')
        vehicleEvents.onUserInactivity(0)

    def standMonitor(self, state):
        if(state == 1):
            self.inactivityTimer.start()
        elif (state == 0):
            self.inactivityTimer.cancel()

    def uiMonitor(self, state):
        if(self.standState == 1 and state == 1):
            self.inactivityTimer.cancel()
            self.inactivityTimer.start()

    def onBikeOff(self):
        subprocess.call('vcgencmd display_power 0', shell=True)
        print('X Started.')
        print('Bike is Off.')

    def onBikeOn(self):
        subprocess.call('vcgencmd display_power 1', shell=True)
        print('Chromium Killed')
        print('Bike is On.')
