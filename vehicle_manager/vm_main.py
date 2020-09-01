import threading
from event_handler import *
from gpio_manager import *
from state_manager import StateManager
from tail_light_controller import TailLightController
from vmgr_compute import *
from carbon_offset import CarbonOffsetCalculator
from quectel import *
import vehicle_states
import time
from gui import *
# from can_handler import *
from ble_agent import *
from ble_advertisement import *
from ble_gatt_server import *
from gps import *
# import signal

# def keyboardInterruptHandler(signal, frame):
#     # print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
#     sys.exit(0)

# signal.signal(signal.SIGINT, keyboardInterruptHandler)
def threadAgent():
    time.sleep(10)
    startAgent()

def threadAdvertisement():
    time.sleep(12)
    startAdvertisementThread()

def threadServer():
    time.sleep(15)
    # vehicleEvents.onBLEReady(1)
    startServer()
    vehicleEvents.onBLEReady(0)

def threadVehicleManager():
    startGUIThread()
    quectel = Quectel.getInstance()
    if(quectel != None):
        gpsMgr = GPS(quectel)
    stateMgr = StateManager.getInstance(GPIOWriter.getInstance())
    # tlContoller = TailLightController(GPIOWriter.getInstance())
    # powerManager = PowerManager()
    gpioReader = GPIOReader.getInstance()
    vmgrComputer = VehicleInfoCalculator()
    carbonOffsetCalculator = CarbonOffsetCalculator()
    # cany = CANHandler(GPIOWriter.getInstance())
    # cany = CANHandler()

if __name__ == '__main__':
    try:
        tAgent = threading.Thread(target = threadAgent)
        tAdvertisement = threading.Thread(target = threadAdvertisement)
        tServer = threading.Thread(target = threadServer)
        tVmgr = threading.Thread(target = threadVehicleManager)

        tVmgr.start()
        # print('After VMGR: number of current threads is ', threading.active_count())
        tAgent.start()
        # print('After Agent: number of current threads is ', threading.active_count())
        tAdvertisement.start()
        # print('After Advertisement: number of current threads is ', threading.active_count())
        tServer.start()
        # print('After Server: number of current threads is ', threading.active_count())
    except KeyboardInterrupt:
        print('Starting Program Cleanup')