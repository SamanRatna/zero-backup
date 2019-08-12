import vehicle_states
import mode_manager
import gpio_manager

class StateManager():

    def __init__(self):
        self.bikeModeMgr = BikeModeManager(gpioMgr)
        self.headLightState = eHeadLightState.HL_OFF
        self.tailLightState = eTailLighteState.TL_OFF
        self.sideLightState = eSideLightState.SL_BOTH_OFF
        self.standState = eStandState.STAND_DOWN
        self.bikeMode = self.bikeModeMgr.getMode()

        self.pinState = {
                        'hibeam':0,
                        'lturn':0,
                        'rturn':0,
                        'lsig':0,
                        'rsig':0,
                        'start_thikka':0,
                        'reverse_suste':0,
                        'babbal':0,
                        'stand':0
                    }
    
    """
    determineHeadLightState:
    """
    def updateHeadLightState(self, hibeam_signal):
        if hibeam_signal == True:
            self.headLightState = eHeadLightState.HL_ON
        else:
            self.headLightState = eHeadLightState.HL_OFF
    
    """
    determineTailLightState:
    """
    def updateTailLightState(self):
        pass

    """
    determineSideLightState:
    """
    def updateSideLightState(self, ls_signal, rs_signal):
        if (ls_signal and rs_signal) == True:
            self.sideLightState = eSideLightState.SL_BOTH_OFF
        elif (ls_signal==True and rs_signal==False):
            self.sideLightState = eSideLightState.SL_RIGHT_ON
        elif (ls_signal==False and rs_signal==True):
            self.sideLightState = eSideLightState.SL_LEFT_ON
        elif (ls_signal or rs_signal) == False:
            self.sideLightState = eSideLightState.SL_BOTH_ON

    """
    determineStandState:
    """
    def updateStandState(self, stand_signal):
        if stand_signal == True:
            self.standState = STAND_DOWN
        else:
            self.standState = STAND_UP

    """
    determineBikeMode:
    """
    def updateBikeMode(self, button, value):
        pass
"""
    def updateState(self, inputChanges, input):
        for change in inputChanges:
            if change == eGPIO.IN_HIBEAM:
                self.updateHeadLightState(input[eGPIO.IN_HIBEAM])
            elif change == eGPIO.IN_LTURN or change == eGPIO.IN_RTURN or change == :
                self.updateSideLightState(input[eGPIO.IN_LTURN],input[eGPIO.IN_RTURN])
            elif change == eGPIO.IN_STAND:
                self.updateStandState(input[eGPIO.IN_STAND])
            elif change == eGPIO.IN_BUTTON_RB or change == eGPIO.IN_BUTTON_RD or change == eGPIO.IN_BUTTON_RU:
                self.updateBikeMode(change, input[change])
            elif change == 
"""

