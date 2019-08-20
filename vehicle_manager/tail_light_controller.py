from vehicle_states import *
from event_handler import *
from gpio_manager import GPIOWriter
import threading

class TailLightController:
    def __init__(self, _gpioWriter):
        self.gpioWriter = _gpioWriter
        self.mode = TLS_Ignition(self)
        self.subscribeToEvents()

    def subscribeToEvents(self):
        vehicleEvents.onIgnition += self.mode.onIgnition
        vehicleEvents.onBrakeToggle += self.mode.onBrake
        vehicleEvents.onLeftSideLightToggle += self.mode.onLeftTurn
        vehicleEvents.onRightSideLightToggle += self.mode.onRightTurn
        vehicleEvents.onCharging += self.mode.onCharging

    def transitionTo(self, _mode):
        self.mode = _mode
        print(self.mode)

class TailLightState:
    def __init__(self, _context):
        self.context = _context
        self.onStateChange()
    def onCharging(self, state):
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
    def __init__(self):
        TailLightState.__init__()
        self.leftTurnState = False
        self.rightTurnState = False

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
            self.leftTurnState = True
            self.righTurnState = False
        else:
            self.context.gpioWriter.setLTurn(True)
            self.leftTurnState = False

    def onRightTurn(self):
        if self.righTurnState = False:
            self.context.gpioWriter.setLTurn(True)
            self.context.gpioWriter.setRTurn(False)
            self.righTurnState = True
            self.leftTurnState = False
        else:
            self.context.gpioWriter.setRTurn(True)
            self.righTurnState = False
    
    def onCharging(self, state):
        if state == False:
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
        ignitionTimer = threading.Timer(3, self.onIgnitionTimer)
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
