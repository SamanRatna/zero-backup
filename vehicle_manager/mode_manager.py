import vehicle_states
from gpio_manager import GPIOWriter

class BikeModeManager:
    def __init__(self, gpioWriter):
        self.mode = ModeStandby(self)
        self.gpioMgr = gpioWriter
        
    def onRightUp(self):
        self.mode.onRightUp()
    
    def onRightDown(self):
        self.mode.onRightDown()
    
    def onRightBack(self):
        self.mode.onRightBack()
    
    def transitionTo(self, state):
        self.mode = state
        self.mode.onStateChange()
        print(self.mode)
    
    def gpioWrite(self, valueStartThikka, valueSuste, valueReverse, valueBabbal, valueCharge):
        pass
        """
        self.gpioMgr.out_start_thikka.write(valueStartThikka)
        self.gpioMgr.out_suste.write(valueSuste)
        self.gpioMgr.out_reverse.write(valueReverse)
        self.gpioMgr.out_babbal.write(valueBabbal)
        self.gpioMgr.out_charge.write(valueCharge)
        """
class BikeMode:

    def __init__(self,_context):
        self.context = _context

    def onRightUp(self):
        pass

    def onRightDown(self):
        pass

    def onRightBack(self):
        pass

    def onStateChange(self):
        pass

class ModeOff(BikeMode):
    def onStateChange(self):
        self.context.gpioWrite(1, 1, 1, 1, 1)

class ModeStandby(BikeMode):
    def onRightUp(self):
        self.context.transitionTo(ModeReverse(self.context))

    def onRightDown(self):
        self.context.transitionTo(ModeThikka(self.context))

    def onStateChange(self):
        self.context.gpioWrite(1, 1, 1, 1, 1)

class ModeSuste(BikeMode):
    def onRightDown(self):
        self.context.transitionTo(ModeThikka(self.context))

    def onRightBack(self):
        self.context.transitionTo(ModeBabbal(self.context))

    def onStateChange(self):
        self.context.gpioWrite(1, 0, 1, 1, 1)

class ModeThikka(BikeMode):
    def onRightUp(self):
        self.context.transitionTo(ModeSuste(self.context))

    def onRightBack(self):
        self.context.transitionTo(ModeBabbal(self.context))

    def onStateChange(self):
        self.context.gpioWrite(0, 1, 1, 1, 1)

class ModeBabbal(BikeMode):
    def onRightUp(self):
        pass

    def onRightDown(self):
        self.context.transitionTo(ModeThikka(self.context))

    def onStateChange(self):
        self.context.gpioWrite(1, 1, 1, 0, 1)

class ModeReverse(BikeMode):
    def onRightDown(self):
        self.context.transitionTo(ModeThikka(self.context))

    def onStateChange(self):
        self.context.gpioWrite(1, 1, 0, 1, 1)

class ModeCharging(BikeMode):
    def onStateChange(self):
        self.context.gpioWrite(1, 1, 1, 1, 0)
