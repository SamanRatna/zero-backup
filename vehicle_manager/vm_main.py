import threading
from event_handler import *
from gpio_manager import *
from state_manager import StateManager
from tail_light_controller import TailLightController
from vmgr_compute import *
import vehicle_states
import threading
import time
from gui import *
from can_handler import *
from ble_advertisement import *
from gatt_server import *
from gps import *
# import signal

# def keyboardInterruptHandler(signal, frame):
#     # print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
#     sys.exit(0)

# signal.signal(signal.SIGINT, keyboardInterruptHandler)

def threadAdvertisement():
    time.sleep(15)
    startAdvertisement()

def threadServer():
    time.sleep(17)
    # vehicleEvents.onBLEReady(1)
    startServer()
    vehicleEvents.onBLEReady(0)

def threadVehicleManager():
    startGUIThread()
    gpsMgr = GPS()
    stateMgr = StateManager.getInstance(GPIOWriter.getInstance())
    # tlContoller = TailLightController(GPIOWriter.getInstance())
    powerManager = PowerManager()
    gpioReader = GPIOReader.getInstance()
    vmgrComputer = VehicleInfoCalculator()
    # cany = CANHandler(GPIOWriter.getInstance())
    cany = CANHandler()
# startGUIThread()
# startAdvertisement()
# startServer()
# stateMgr = StateManager.getInstance(GPIOWriter.getInstance())
# tlContoller = TailLightController(GPIOWriter.getInstance())
# gpioReader = GPIOReader.getInstance()
# cany = CANHandler(GPIOWriter.getInstance())
# vmgrComputer = VehicleInfoCalculator()

if __name__ == '__main__':
    try:
        tAdvertisement = threading.Thread(target = threadAdvertisement)
        tServer = threading.Thread(target = threadServer)
        tVmgr = threading.Thread(target = threadVehicleManager)
        tVmgr.start()
        tAdvertisement.start()
        tServer.start()
    except KeyboardInterrupt:
        print('Starting Program Cleanup')