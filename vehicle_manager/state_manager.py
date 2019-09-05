from vehicle_states import *
from mode_manager import BikeModeManager
from gpio_manager import GPIOWriter
from event_handler import *

class StateManager():

    __instance = None
    @staticmethod
    def getInstance(gpioWriter):
        if StateManager.__instance == None:
            StateManager(gpioWriter)
        return StateManager.__instance

    def __init__(self,gpioWriter):
        if StateManager.__instance == None:
            #raise Exception("StateManager is a Singleton Class.")
        #else:
            StateManager.__instance = self
            self.bikeModeMgr = BikeModeManager(gpioWriter)
            
            self.headLightState = eHeadLightState.HL_OFF
            self.tailLightState = eTailLightState.TL_OFF
            self.sideLightState = eSideLightState.SL_BOTH_OFF
            self.standState = eStandState.STAND_DOWN

            self.subscribeToEvents()
    
    def subscribeToEvents(self):
        vehicleEvents.onRUPress += self.bikeModeMgr.onRightUp
        vehicleEvents.onRDPress += self.bikeModeMgr.onRightDown
        vehicleEvents.onRBPress += self.bikeModeMgr.onRightBack
        vehicleEvents.onRDHold += self.bikeModeMgr.onRightDownHold

        vehicleEvents.onStandSwitch += self.updateStandState
        """
        vehicleEvents.onRightSideLightToggle += self.updateSideLightState
        vehicleEvents.onLeftSideLightToggle += self.updateSideLightState
        """
        vehicleEvents.onHibeamToggle += self.updateHeadLightState

    def updateHeadLightState(self, hibeam_signal):
        if hibeam_signal == 0:
            self.headLightState = eHeadLightState.HL_HI_BEAM
        else:
            self.headLightState = eHeadLightState.HL_LOW_BEAM
        print(self.headLightState)

    """
    def updateSideLightState(self, signal):
        if (ls_signal and rs_signal) == True:
            self.sideLightState = eSideLightState.SL_BOTH_OFF
        elif (ls_signal==True and rs_signal==False):
            self.sideLightState = eSideLightState.SL_RIGHT_ON
        elif (ls_signal==False and rs_signal==True):
            self.sideLightState = eSideLightState.SL_LEFT_ON
        elif (ls_signal or rs_signal) == False:
            self.sideLightState = eSideLightState.SL_BOTH_ON
        print(self.sideLightState)
    """

    def updateStandState(self, stand_signal):
        if stand_signal == 0:
            self.standState = eStandState.STAND_UP
        else:
            self.standState = eStandState.STAND_DOWN
        print(self.standState)
