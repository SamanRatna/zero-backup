from enum import Enum

class eHeadLightState(Enum):
    HL_OFF = 0
    HL_LOW_BEAM = 1
    HL_HI_BEAM = 2
    HL_PASS_LIGHT = 3

class eBikeMode(Enum):
    MODE_OFF = 0
    MODE_STANDBY = 1
    MODE_REVERSE = 2
    MODE_SUSTE = 3
    MODE_THIKKA = 4
    MODE_BABBAL = 5
    MODE_CHARGING = 6
    MODE_INVALID = 7

class eSideLightState(Enum):
    SL_BOTH_OFF = 0
    SL_RIGHT_ON = 1
    SL_LEFT_ON = 2
    SL_BOTH_ON = 3

class eStandState(Enum):
    STAND_UP = 0
    STAND_DOWN = 1

class eTailLightState(Enum):
    TL_OFF = 1
    TL_NORMAL = 2
    TL_LEFT_TURN = 4
    TL_RIGHT_TURN = 8
    TL_BRAKE = 16

class eTailLightSectionState(Enum):
    TLS_OFF = 0
    TLS_LR = 1
    TLS_BR = 2

class eGPIO(Enum):
    IN_HIBEAM = 1
    IN_LTURN = 2
    IN_RTURN = 3
    IN_BUTTON_RD = 4
    IN_BUTTON_RU = 5
    IN_BUTTON_RB = 6
    IN_STAND = 7
