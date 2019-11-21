from vehicle_states import *
from gpio_manager import GPIOWriter
from gui import *

class BikeModeManager:
    def __init__(self, gpioWriter):
        self.mode = ModeStandby(self)
        self.gpioMgr = gpioWriter
        self.mode.onStateChange()
        print(self.mode)
    
    def onCharging(self, status):
        self.mode.onCharge(status)

    def onRightUp(self):
        self.mode.onRightUp()
    
    def onRightDown(self):
        self.mode.onRightDown()

    def onRightDownHold(self):
        self.mode.onRightDownHold()
    
    def onRightBack(self):
        self.mode.onRightBack()
    
    def transitionTo(self, state):
        self.mode = state
        self.mode.onStateChange()
        print(self.mode)
    
    def setMode(self, mode):
        self.gpioMgr.setMode(mode)
        publishBikeMode(mode)

class BikeMode:

    def __init__(self,_context):
        self.context = _context

    def onCharge(self, status):
        pass
        
    def onRightUp(self):
        pass

    def onRightDown(self):
        pass

    def onRightDownHold(self):
        pass

    def onRightBack(self):
        pass

    def onStateChange(self):
        pass

class ModeOff(BikeMode):
    def onStateChange(self):
        pass

class ModeStandby(BikeMode):
    def onRightBack(self):
        self.context.transitionTo(ModeReverse(self.context))

    def onRightDown(self):
        self.context.transitionTo(ModeThikka(self.context))

    def onCharge(self, status):
        if(status == 'charging'):
            self.context.transitionTo(ModeCharging(self.context))

    def onStateChange(self):
        self.context.setMode(eBikeMode.MODE_STANDBY)
    

class ModeSuste(BikeMode):
    def onRightDown(self):
        self.context.transitionTo(ModeThikka(self.context))

    def onRightBack(self):
        self.context.transitionTo(ModeBabbal(self.context))

    def onStateChange(self):
        self.context.setMode(eBikeMode.MODE_SUSTE)

class ModeThikka(BikeMode):
    def onRightUp(self):
        self.context.transitionTo(ModeSuste(self.context))

    def onRightDownHold(self):
        self.context.transitionTo(ModeStandby(self.context))

    def onRightBack(self):
        self.context.transitionTo(ModeBabbal(self.context))

    def onStateChange(self):
        self.context.setMode(eBikeMode.MODE_THIKKA)

class ModeBabbal(BikeMode):
    def onRightUp(self):
        pass

    def onRightDown(self):
        self.context.transitionTo(ModeThikka(self.context))

    def onStateChange(self):
        self.context.setMode(eBikeMode.MODE_BABBAL)

class ModeReverse(BikeMode):
    def onRightDown(self):
        self.context.transitionTo(ModeThikka(self.context))

    def onStateChange(self):
        self.context.setMode(eBikeMode.MODE_REVERSE)

class ModeCharging(BikeMode):
    def onCharge(self, status):
        if(status == 'discharging'):
            self.context.transitionTo(ModeStandby(self.context))

    def onStateChange(self):
        self.context.setMode(eBikeMode.MODE_CHARGING)
