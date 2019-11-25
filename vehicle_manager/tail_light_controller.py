from vehicle_states import *
from event_handler import *
from gpio_manager import GPIOWriter
import threading
from gui import *

class TailLightController:
    def __init__(self, _gpioWriter):
        self.gpioWriter = _gpioWriter
        self.mode = TLS_Ignition(self)
        self.subscribeToEvents()

    def subscribeToEvents(self):
        #vehicleEvents.onIgnition += self.onIgnition
        vehicleEvents.onBrakeToggle += self.onBrake
        vehicleEvents.onLeftSideLightToggle += self.onLeftTurn
        vehicleEvents.onRightSideLightToggle += self.onRightTurn
        vehicleEvents.onCharging += self.onCharging

    def transitionTo(self, _mode):
        self.mode = _mode
        print(self.mode)

    def onBrake(self, state):
        self.mode.onBrake(state)

    def onLeftTurn(self, value):
        self.mode.onLeftTurn()

    def onRightTurn(self, value):
        self.mode.onRightTurn()

    def onCharging(self, state):
        self.mode.onCharging(state)

class TailLightState:
    def __init__(self, _context):
        self.context = _context
        self.onStateChange()
    def onCharging(self, state):
        pass
    def onIgnition(self, state):
        pass
    def onLeftTurn(self):
        pass
    def onRightTurn(self):
        pass
    def onBrake(self, state):
        pass
    def onStateChange(self):
        pass
        
class TLS_Normal(TailLightState):
    def __init__(self, _context):
        TailLightState.__init__(self,_context)
        self.leftTurnState = False
        self.rightTurnState = False
    def setTurnStates(self, left, right):
        self.leftTurnState = left
        self.rightTurnState = right
        print('self.leftTurnState: ', self.leftTurnState)
        print('self.rightTurnState: ', self.rightTurnState)
        
    def onStateChange(self):
        self.context.gpioWriter.setIgn(True)
        self.context.gpioWriter.setCharge(True)
        self.context.gpioWriter.setBrake(True)
        self.context.gpioWriter.setLTurn(True)
        self.context.gpioWriter.setRTurn(True)

    def onBrake(self, brakeState):
        self.context.gpioWriter.setBrake(brakeState)

    def onLeftTurn(self):
        if self.leftTurnState == False:
            self.context.gpioWriter.setRTurn(True)
            self.context.gpioWriter.setLTurn(False)
            self.setTurnStates(True, False)
            publishSideLightStatus('left')
            print("Turning Left...")
 
        else:
            self.context.gpioWriter.setLTurn(True)
            self.setTurnStates(False, False)
            publishSideLightStatus('off')
            print("Stopped turning Left...")


    def onRightTurn(self):
        if self.rightTurnState == False:
            self.context.gpioWriter.setLTurn(True)
            self.context.gpioWriter.setRTurn(False)
            self.setTurnStates(False,True)
            publishSideLightStatus('right')
            print("Turning Right...")
        else:
            self.context.gpioWriter.setRTurn(True)
            self.setTurnStates(False, False)
            publishSideLightStatus('off')
            print("Stopped turning Right...")

    def onCharging(self, state):
        if state == 'charging':
            self.context.transitionTo(TLS_Charging(self.context))
        else:
            self.context.transitionTo(TLS_Normal(self.context))

    def onIgnition(self, state):
        self.context.transitionTo(TLS_Ignition(self.context))

class TLS_Ignition(TailLightState):
    def onStateChange(self):
        self.context.gpioWriter.setCharge(True)
        self.context.gpioWriter.setBrake(True)
        self.context.gpioWriter.setLTurn(True)
        self.context.gpioWriter.setRTurn(True)
        self.context.gpioWriter.setIgn(False)
        ignitionTimer = threading.Timer(5, self.onIgnitionTimer)
        ignitionTimer.start()
    
    def onIgnitionTimer(self):
        self.context.transitionTo(TLS_Normal(self.context))

class TLS_Charging(TailLightState):
    def onStateChange(self):
        self.context.gpioWriter.setBrake(True)
        self.context.gpioWriter.setLTurn(True)
        self.context.gpioWriter.setRTurn(True)
        self.context.gpioWriter.setIgn(True)
        self.context.gpioWriter.setCharge(False)
