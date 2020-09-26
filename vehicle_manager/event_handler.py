from events import Events
import threading

class VehicleEvents(Events):
    __events__ = ('onRUPress','onRDPress', 'onRDHold', 'onRBPress', 'onHibeamToggle', 'onRightSideLightToggle', 'onLeftSideLightToggle', 'onBrakeToggle', 'onStandSwitch', 'onIgnition', 'onCharging', 'onTripReset', 'onBLEReady', 'onUserInteraction', 'onUserInactivity', 'onCarbonOffsetRequest', 'onBrightnessChange', 'confirmBluetoothPairing', 'onBluetoothPairingConfirmation', 'onBluetoothConnection', 'onNavigation', 'onBluetooth', 'guiReady', 'onBluetoothNameChange', 'finder','swupdate','swupdateResponse', 'bikeOn', 'bikeOff')

class VehicleReadings(Events):
    __events__ = ('odoReading','speedReading', 'maxSpeed', 'tripMaxSpeed', 'averageSpeeds', 'distances', 'batteryStatus', 'batteryTemperature', 'motorTemperature', 'controllerTemperature', 'packVoltage', 'gpsLocation' , 'carbonOffset', 'carbonOffsetForBluetooth', 'heading', 'bleDevices', 'network', 'bikeMode')

vehicleEvents = VehicleEvents()
vehicleReadings = VehicleReadings()

def eventOdoReading(value):
    print("Odo Reading: ", value)

def eventSpeedReading(value):
    print("Speed Reading: ", value)

def eventMaxSpeed(value):
    print("Max Speed: ", value)

def eventAverageSpeeds(value1, value2):
    print("Average Speeds: ", value1, value2)

def eventDistances(value1, value2):
    print("Distances: ", value1, value2)

def eventRUPress():
    print("RU Press Event Triggered.")

def eventRBPress():
    print("RB Press Event Triggered.")

def eventRDPress():
    print("RD Press Event Triggered.")

def eventRDHold():
    print("RD Hold Event Triggered.")

def eventLeftTurn(value):
    print("Left Turn Toggled: ", str(value))

def eventRightTurn(value):
    print("Right Turn Toggled: ", str(value))

def eventStand(state):
    print("Stand Toggled: " + str(state) )

def eventBrake(state):
    print("Brake Toggled: " + str(state))

def eventHibeam(state):
    print("Hibeam toggled: " + str(state))

def eventTripReset():
    print("Trip Reset Requested")

def eventBatteryStatus(value):
    print('Battery Status: ', str(value))
    
def eventBLEReady(value):
    print('BLE Status: ', str(value))

def eventUserInteraction(state):
    print('User Activity: ', str(state))

def readingGPSLocation(lat, lon):
    print('Latitude: ', lat)
    print('Longitude: ', lon)

def readingCarbonOffset(data):
    print(data)

def confirmBluetoothPairing(data):
    print(data)
def respondBluetoothPairing(data):
    print(data)
def bluetoothConnection(name, data):
    print("Bluetooth Connection: ",name, data)
def navigationRequest(request):
    print('Navigation Request: ', request)
def bluetoothRequest(request):
    print('Bluetooth Request: ', request)
def onFinder(value):
    print('Find Request: ', value)
def onswupdate(message):
    print('Software Update: ', message)
def onBikeOff():
    print('Bike is Off.')
def onBikeOn():
    print('Bike is On.')
vehicleEvents.onRUPress += eventRUPress
vehicleEvents.onRBPress += eventRBPress
vehicleEvents.onRDPress += eventRDPress
vehicleEvents.onHibeamToggle += eventHibeam
vehicleEvents.onRightSideLightToggle += eventRightTurn
vehicleEvents.onLeftSideLightToggle += eventLeftTurn
vehicleEvents.onBrakeToggle += eventBrake
vehicleEvents.onStandSwitch += eventStand
vehicleEvents.onRDHold += eventRDHold
vehicleEvents.onTripReset += eventTripReset
# vehicleReadings.odoReading += eventOdoReading
# vehicleReadings.speedReading += eventSpeedReading
# vehicleReadings.maxSpeed += eventMaxSpeed
# vehicleReadings.averageSpeeds += eventAverageSpeeds
# vehicleReadings.distances += eventDistances
# vehicleReadings.batteryStatus += eventBatteryStatus
vehicleEvents.onBLEReady += eventBLEReady
vehicleEvents.onUserInteraction += eventUserInteraction
vehicleReadings.gpsLocation += readingGPSLocation
vehicleReadings.carbonOffset += readingCarbonOffset
vehicleEvents.confirmBluetoothPairing += confirmBluetoothPairing
vehicleEvents.onBluetoothPairingConfirmation += respondBluetoothPairing
vehicleEvents.onBluetoothConnection += bluetoothConnection
vehicleEvents.onNavigation += navigationRequest
vehicleEvents.onBluetooth += bluetoothRequest
vehicleEvents.finder += onFinder
vehicleEvents.swupdate += onswupdate
vehicleEvents.bikeOff += onBikeOff
vehicleEvents.bikeOn += onBikeOn