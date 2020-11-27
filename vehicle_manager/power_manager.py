from event_handler import *
import threading
from gpio_manager import RepeatableTimer
import os

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
        pass
        # os.system('tvservice -o')
        # os.system('systemctl stop guix.service')

    def onBikeOn(self):
        pass
        # os.system('tvservice -p')
        # os.system('systemctl start guix.service')
