import eel
import threading
import multiprocessing
import os
import time
# import netifaces
import logging
from event_handler import *
# from power_manager import *
from api_handler import *
from quectel import *
#Configure logger
# logging.basicConfig(filemode='a')
chargeLogger=logging.getLogger('event-logger')
chargeLogger.setLevel(logging.WARNING)
eel.init('gui-revised')
# maxSpeed = 0
# bikeMode = "MODE_STANDBY"
# bluetooth = 0
# bluetoothName = ' '
# networkInfo = None
# my_options = {
#     'mode': "chrome", #or "chrome-app",
#     'host': 'localhost',
#     'port': 8080,
#     'chromeFlags': ["--start-fullscreen", "--browser-startup-dialog"]
# }
def startGUI():
    try:
        eel.start('index.html', mode=False, host='0.0.0.0')
        # eel.start('index.html', mode=False)
    except (SystemExit, MemoryError, KeyboardInterrupt):
        pass
    print ('This is printed when the window is closed!')
    startGUI()

def publishBikeMode(mode):
    # global bikeMode
    eel.updateBikeMode(mode.name)
    # bikeMode = mode.name

# def publishLeftTurnStatus(status):
#     if status==True:
#         eel.updateLeftTurnStatus(1)
#     else:
#         eel.updateLeftTurnStatus(0)

# def publishRightTurnStatus(status):
#     if status==True:
#         eel.updateRightTurnStatus(1)
#     else:
#         eel.updateRightTurnStatus(0)

# def publishSideLightStatus(status):
#     eel.updateSideLight(status)

# def publishBeamStatus(status):
#     eel.updateBeam(status.name)

def publishSpeedPower(speed, power):
    eel.updateSpeedPower(round(speed), round(power))

def publishSOC(soc, rangeSuste, rangeThikka, rangeBabbal):
    eel.updateSOC(round(soc), round(rangeSuste), round(rangeThikka), round(rangeBabbal))

def publishChargingStatus(status, current, timeToCharge):
    eel.updateChargingStatus(status, current, timeToCharge)

def publishMaxSpeed(value):
    # global maxSpeed
    eel.updateMaxSpeed(round(value))
    # maxSpeed = value

def publishAverageSpeeds(odoAverage, tripAverage):
    eel.updateAverageSpeeds(round(odoAverage), round(tripAverage))

def publishDistances(odometer, tripDistance):
    eel.updateDistances(round(odometer), round(tripDistance))

def publishAdvertisementStatus(status):
    eel.updateAdvertisementStatus(status)
    # global bluetooth
    # global bluetoothName
    # bluetooth = status[0]
    if(len(status) > 1):
        # bluetoothName = status[1]
        print(status[1])

def publishBluetoothStatus(name, status):
    eel.updateBluetoothStatus(name, status)

def publishBatteryTemperature(temp):
    eel.updateBatteryTemperature(temp)
    # print('Battery Temperature: ', str(temp))

def publishMotorTemperature(temp):
    eel.updateMotorTemperature(temp)
    # print('Motor Temperature: ', str(temp))

def publishControllerTemperature(temp):
    eel.updateControllerTemperature(temp)
    # print('Controller Temperature: ', str(temp))

def publishPackVoltage(voltage):
    eel.updatePackVoltage(voltage)

def publishStandState(state):
    eel.updateStandState(state)

def publishCarbonOffset(data):
    print('Publishing Carbon Offset Data')
    eel.updateCarbonOffset(data)

def startGUIThread():
    try:        
        guiThread = threading.Thread(target=startGUI)
        guiThread.start()
    except:
        print("Error: Unable to start the GUI thread.")

def publishCurrentLocation(lat, lon):
    data = [lat, lon, 'None']
    eel.updateBearing(data)

def publishHeading(data):
    eel.updateBearing(data)

def requestForBluetoothPairingConfirmation(passkey):
    # print('Requesting for Bluetooth: ', passkey)
    eel.requestBluetoothPairingConfirmation(passkey)

def publishNetworkInfo(info):
    # global networkInfo
    # print(info)
    # networkInfo = info
    eel.updateNetworkInfo(info)

def initializeLocation(lat, lon):
    data = [lat, lon, 'None']
    eel.onLocationResponse(data)

@eel.expose
def bluetoothPairingConfirmation(response):
    # print('Response for Bluetooth: ', response)
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
    # print('Brigtness: ', brightness)

@eel.expose
def getAPIKey():
    print('API Request Received')
    api = returnAPI()
    return(api)

@eel.expose
def getCurrentLocation(status):
    if(status == True):
        vehicleReadings.gpsLocation += initializeLocation
    else:
        vehicleReadings.gpsLocation -= initializeLocation
    vehicleEvents.onNavigation(status)

@eel.expose
def startFastCharge(option):
    if(option == 0):
        print('Option Not available yet.')
        return;
    pFastCharge = multiprocessing.Process(target = fastCharge, args=(option,))
    pFastCharge.start()
    pFastCharge.join()
    print('Finished the charge process.')

def fastCharge(option):
    count = 1200*option
    while(count > 0):
        chargeLogger.warning('Sending')
        os.system('cansend can0 300#01E8034C04AA00')
        time.sleep(0.05)
        count = count - 1
def publishBluetoothDevices(devices):
    eel.updateBluetoothDevices(devices)

def publishFinder(command):
    eel.updateFinderRequest(command)

@eel.expose
def getConnectivityStatus():
    print('Getting Connectivity Status')
    iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    ip = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
    eel.updateConnectivityStatus(iface, ip)

@eel.expose
def resetTripData():
    print('Trip Reset Requested.')
    vehicleEvents.onTripReset()

@eel.expose
def getGUIData():
    vehicleEvents.guiReady()
    # global maxSpeed
    # global bikeMode
    # global bluetooth
    # global bluetoothName
    # global networkInfo
    # eel.updateBikeMode(bikeMode)
    # publishMaxSpeed(maxSpeed)
    # publishAdvertisementStatus([bluetooth, bluetoothName])
    # publishNetworkInfo(networkInfo)

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
    vehicleEvents.onNavigation(request)
    if(request == True):
        vehicleReadings.gpsLocation += publishCurrentLocation
    elif(request == False):
        vehicleReadings.gpsLocation -= publishCurrentLocation

@eel.expose
def changeBluetoothName(name):
    vehicleEvents.onBluetoothNameChange(name)

vehicleReadings.bikeMode += publishBikeMode
vehicleReadings.maxSpeed += publishMaxSpeed
vehicleReadings.averageSpeeds += publishAverageSpeeds
vehicleReadings.distances += publishDistances
vehicleEvents.onBLEReady += publishAdvertisementStatus
vehicleReadings.batteryTemperature += publishBatteryTemperature
vehicleReadings.motorTemperature += publishMotorTemperature
vehicleReadings.controllerTemperature += publishControllerTemperature
vehicleReadings.packVoltage += publishPackVoltage
vehicleEvents.onStandSwitch += publishStandState
vehicleReadings.carbonOffset += publishCarbonOffset
# vehicleReadings.gpsLocation += publishCurrentLocation
vehicleReadings.heading += publishHeading
vehicleEvents.confirmBluetoothPairing += requestForBluetoothPairingConfirmation
vehicleEvents.onBluetoothConnection += publishBluetoothStatus
vehicleReadings.bleDevices += publishBluetoothDevices
vehicleReadings.network += publishNetworkInfo
vehicleEvents.finder += publishFinder
if __name__ == "__main__":
    startGUIThread()