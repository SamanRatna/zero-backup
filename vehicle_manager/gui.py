import eel
import math
import threading
import multiprocessing
import os
import time
import logging
from event_handler import *
from api_handler import *

#Configure logger
# logging.basicConfig(filemode='a')
chargeLogger=logging.getLogger('event-logger')
chargeLogger.setLevel(logging.WARNING)
eel.init('gui-revised')

ignitionState = True
bikeModeMemory = 2
chargingStateMemory = False
fastChargingStateMemory = False

def startGUI():
    try:
        eel.start('index.html', mode=False, host='0.0.0.0')
        # eel.start('index.html', mode=False)
    except (SystemExit, MemoryError, KeyboardInterrupt):
        pass
    print ('This is printed when the window is closed!')
    startGUI()

def publishBikeMode(mode):
    global bikeModeMemory
    bikeModeMemory = mode
    bikeMode = 'None'
    if(mode == 1):
        bikeMode = 'MODE_REVERSE'
    elif(mode == 2):
        bikeMode = 'MODE_STANDBY'
    elif(mode == 3):
        bikeMode = 'MODE_SUSTE'
    elif(mode == 4):
        bikeMode = 'MODE_THIKKA'
    elif(mode == 5):
        bikeMode = 'MODE_BABBAL'
    eel.updateBikeMode(bikeMode)

def publishSideLightStatus(status):
    eel.updateTurnSignal(status)

def publishHeadLightStatus(light, status):
    eel.updateHeadlightSignal(light, status)

def publishSpeedPower(speed, power):
    eel.updateSpeedPower(int(speed), round(power))

def publishSOC(soc, soh,rangeSuste, rangeThikka, rangeBabbal):
    eel.updateSOC(math.floor(soc), math.floor(soh), rangeSuste, rangeThikka, rangeBabbal)

def publishChargingStatus(isCharging, isFastCharging):
    global chargingStateMemory, fastChargingStateMemory
    chargingStateMemory = isCharging
    fastChargingStateMemory = isFastCharging
    eel.updateChargingStatus(isCharging, isFastCharging)

def publishMaxSpeed(value):
    eel.updateMaxSpeed(round(value))

def publishTripMaxSpeed(value):
    eel.updateTripMaxSpeed(round(value))

def publishAverageSpeeds(odoAverage, tripAverage):
    eel.updateAverageSpeeds(round(odoAverage), round(tripAverage))

def publishDistances(odometer, tripDistance):
    eel.updateDistances(math.floor(odometer), math.floor(tripDistance))

def publishBluetoothStatus(status):
    eel.updateAdvertisementStatus(status)

def publishBluetoothConnectionStatus(name, status):
    eel.updateBluetoothStatus(name, status)

def publishBatteryTemperature(temp):
    eel.updateBatteryTemperature(temp)

def publishMotorTemperature(motorTemp, controllerTemp):
    eel.updateMotorTemperature(motorTemp, controllerTemp)

def publishVCUTemperature(uc, power):
    eel.updateVCUTemperature(uc, power)

def publishPackVoltage(voltage):
    eel.updatePackVoltage(voltage)

def publishStandState(state):
    eel.updateStandState(state)

def publishCarbonOffset(coSum, data):
    print('Publishing Carbon Offset Data')
    eel.updateCarbonOffset(coSum, data)

def startGUIThread():
    try:        
        guiThread = threading.Thread(target=startGUI)
        guiThread.start()
    except:
        print("Error: Unable to start the GUI thread.")

def publishCurrentLocation(hasFix, lat, lon):
    data = [lat, lon]
    eel.updateLocation(hasFix, data)

def publishOrientationData(heading, roll, pitch):
    eel.updateOrientation(heading,roll,pitch)

def requestForBluetoothPairingConfirmation(passkey):
    eel.requestBluetoothPairingConfirmation(passkey)

def publishNetworkInfo(info):
    eel.updateNetworkInfo(info)

def initializeLocation(hasFix, lat, lon):
    data = [lat, lon, 'None']
    eel.onLocationResponse(hasFix, data)

@eel.expose
def bluetoothPairingConfirmation(response):
    vehicleEvents.onBluetoothPairingConfirmation(response)

@eel.expose
def rebootBoard():
    print('Rebooting the computer...')
    os.system('sudo shutdown -h now')

@eel.expose
def initCarbonOffset():
    print('Initialization of carbon offset requested...')
    vehicleEvents.onCarbonOffsetRequest(0)

@eel.expose
def changeBrightness(brightness):
    vehicleEvents.onBrightnessChange(brightness)

@eel.expose
def getAPIKey():
    print('API Request Received')
    api = returnAPI()
    return(api)

@eel.expose
def getCurrentLocation(status):
    print('GetCurrentLocation called with status: ', status)
    if(status == True):
        vehicleReadings.gpsLocation += initializeLocation
    else:
        vehicleReadings.gpsLocation -= initializeLocation
    vehicleEvents.onNavigation(status)

def publishBluetoothDevices(devices):
    eel.updateBluetoothDevices(devices)

def publishFinder(command):
    print('GUI: publishFinder: ', command)
    eel.updateFinderRequest(command)

def publishSWUpdate(message):
    eel.requestSWUpdateConfirmation(message)

@eel.expose
def onSettingsPage():
    vehicleEvents.refreshSettingsData()

@eel.expose
def swupdateResponse(response):
    vehicleEvents.swupdateResponse(response)

@eel.expose
def resetTripData():
    vehicleEvents.onTripReset()

@eel.expose
def getGUIData():
    vehicleEvents.guiReady()
    global ignitionState, bikeModeMemory, chargingStateMemory, fastChargingStateMemory
    publishBikeOnOffStatus(ignitionState)
    eel.updateChargingStatus(chargingStateMemory, fastChargingStateMemory)
    publishBikeMode(bikeModeMemory)

@eel.expose
def changeBluetoothState(toState):
    print('GUI: Received request to change bluetooth state to: ', toState)
    vehicleEvents.onBluetooth(toState)

@eel.expose
def updateUserActivityStatus(status):
    vehicleEvents.onUserInteraction(status)

@eel.expose
def getNetworkInfo():
    info = Quectel.getInstance().getSimInfo()

@eel.expose
def setGPS(state):
    if(state == True):
        Quectel.getInstance().enableGPS()
    else:
        Quectel.getInstance().disableGPS()

@eel.expose
def requestLocationHeading(request):
    print('Request Location Heading: ', request)
    if(request == True):
        vehicleReadings.gpsLocation += publishCurrentLocation
    elif(request == False):
        vehicleReadings.gpsLocation -= publishCurrentLocation
    vehicleEvents.onNavigation(request)

@eel.expose
def changeBluetoothName(name):
    vehicleEvents.onBluetoothNameChange(name)

def publishBluetoothName(name):
    eel.updateBluetoothName(name)

def publishFuelSavings(data):
    eel.updateFuelSavings(data)

def publishRiderInfo(info):
    eel.updateRiderInfo(info)

@eel.expose
def fetchRiderInfo():
    vehicleEvents.fetchRiderInfo()

@eel.expose
def checkInternetConnectivity():
    vehicleEvents.checkInternetConnectivity()

def publishBikeOnOffStatus(state):
    global ignitionState
    ignitionState = state
    eel.updateBikeOnOffStatus(state)

vehicleReadings.bikeMode += publishBikeMode
vehicleReadings.maxSpeed += publishMaxSpeed
vehicleReadings.tripMaxSpeed += publishTripMaxSpeed
vehicleReadings.averageSpeeds += publishAverageSpeeds
vehicleReadings.distances += publishDistances
vehicleEvents.bluetoothStatus += publishBluetoothStatus
vehicleReadings.batteryTemperature += publishBatteryTemperature
vehicleReadings.motorTemperature += publishMotorTemperature
vehicleReadings.vcuTemperature += publishVCUTemperature
vehicleReadings.packVoltage += publishPackVoltage
vehicleEvents.onStandSwitch += publishStandState
vehicleReadings.carbonOffset += publishCarbonOffset
vehicleEvents.confirmBluetoothPairing += requestForBluetoothPairingConfirmation
vehicleEvents.onBluetoothConnection += publishBluetoothConnectionStatus
vehicleReadings.bleDevices += publishBluetoothDevices
vehicleReadings.network += publishNetworkInfo
vehicleEvents.finder += publishFinder
vehicleEvents.swupdate += publishSWUpdate
vehicleReadings.orientation += publishOrientationData
vehicleEvents.bluetoothName += publishBluetoothName
vehicleReadings.fuelSavings += publishFuelSavings
vehicleReadings.riderInfo += publishRiderInfo
vehicleEvents.onSideLight += publishSideLightStatus
vehicleEvents.onHeadLight += publishHeadLightStatus
vehicleEvents.charging += publishChargingStatus
vehicleEvents.bikeOnOff += publishBikeOnOffStatus
vehicleReadings.socRange += publishSOC
# ########### For development only ########### #
def publishSpeed(speed):
    eel.updateSpeedPower(speed, speed)

vehicleReadings.speedReading += publishSpeed
#################################################

if __name__ == "__main__":
    startGUIThread()
