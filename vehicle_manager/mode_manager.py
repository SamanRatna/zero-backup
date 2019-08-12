import vehicle_states
from gpio_manager import GPIOManager

class BikeModeManager:
    def __init__(self, gpioManager):
        self.mode = eBikeMode.MODE_OFF
        self.gpioMgr = gpioManager
    def getMode(self):
        return self.mode

    def evaluateInput(self, input):
        pass

    def gpioWrite(self, valueStartThikka, valueSuste, valueReverse, valueBabbal, valueCharge):
        self.gpioMgr.out_start_thikka.write(valueStartThikka)
        self.gpioMgr.out_suste.write(valueSuste)
        self.gpioMgr.out_reverse.write(valueReverse)
        self.gpioMgr.out_babbal.write(valueBabbal)
        self.gpioMgr.out_charge.write(valueCharge)

class BikeMode:
    def onRightUp(self):
        return eBikeMode.MODE_INVALID

    def onRightDown(self):
        return eBikeMode.MODE_INVALID

    def onRightBack(self):
        return eBikeMode.MODE_INVALID

    def onStateChange(self):
        pass

class ModeOff(BikeMode):
    def onStateChange(self):
        return [1, 1, 1, 1, 1]

class ModeStandby(BikeMode):
    def onRightUp(self):
        return eBikeMode.MODE_REVERSE

    def onRightDown(self):
        return eBikeMode.MODE_THIKKA

    def onStateChange(self):
        return [1, 1, 1, 1, 1]

class ModeSuste(BikeMode):
    def onRightDown(self):
        return eBikeMode.MODE_THIKKA

    def onRightBack(self):
        return eBikeMode.MODE_BABBAL

    def onStateChange(self):
        return [1, 0, 1, 1, 1]

class ModeThikka(BikeMode):
    def onRightUp(self):
        return eBikeMode.MODE_SUSTE

    def onRightBack(self):
        return eBikeMode.MODE_BABBAL

    def onStateChange(self):
        return [0, 1, 1, 1, 1]

class ModeBabbal(BikeMode):
    def onRightUp(self):
        return eBikeMode.MODE_INVALID

    def onRightDown(self):
        return eBikeMode.MODE_THIKKA

    def onStateChange(self):
        return [1, 1, 1, 0, 1]

class ModeReverse(BikeMode):
    def onRightDown(self):
        return eBikeMode.MODE_THIKKA

    def onStateChange(self):
        return [1, 1, 0, 1, 1]

class ModeCharging(BikeMode):
    def onStateChange(self):
        return [1, 1, 1, 1, 0]
