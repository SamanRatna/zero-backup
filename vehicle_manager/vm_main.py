import threading
from event_handler import *
from gpio_manager import *
# from state_manager import StateManager
# from tail_light_controller import TailLightController
# from vmgr_compute import *
from power_manager import *
from carbon_offset import CarbonOffsetCalculator
from quectel import *
import vehicle_states
import time
from gui import *
from can_handler import *
from ble_agent import *
from ble_advertisement import *
from ble_gatt_server import *
from gps import *
from orientation import Orientation
from sw_update import *
from ble_adapter import *

# import signal

try:
    import dummy_data
except:
    pass

# def keyboardInterruptHandler(signal, frame):
#     # print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
#     sys.exit(0)

# signal.signal(signal.SIGINT, keyboardInterruptHandler)
def threadAgent():
    time.sleep(2)
    startAgent()

def threadAdvertisement():
    time.sleep(4)
    startAdvertisementThread()

def threadServer():
    time.sleep(6)
    # vehicleEvents.onBLEReady(1)
    startServer()
    vehicleEvents.onBLEReady(0)

def threadDiscovery():
    time.sleep(8)
    setDiscovery(True)

def threadVehicleManager():
    startGUIThread()
    # quectel = Quectel.getInstance()
    # if(quectel != None):
    #     gpsMgr = GPS(quectel)
    # stateMgr = StateManager.getInstance(GPIOWriter.getInstance())
    # tlContoller = TailLightController(GPIOWriter.getInstance())
    # powerManager = PowerManager()
    # gpioReader = GPIOReader.getInstance()
    # gpioWriter = GPIOWriter.getInstance()
    # vmgrComputer = VehicleInfoCalculator()
    # carbonOffsetCalculator = CarbonOffsetCalculator()
    # orientation = Orientation.getInstance()
    # cany = CANHandler(GPIOWriter.getInstance())
    cany = CANHandler()

def threadSWUpdate():
    swupdate()

if __name__ == '__main__':
    try:
        tAgent = threading.Thread(target = threadAgent)
        tAdvertisement = threading.Thread(target = threadAdvertisement)
        tServer = threading.Thread(target = threadServer)
        tVmgr = threading.Thread(target = threadVehicleManager)
        tSWUpdate = threading.Thread(target=threadSWUpdate)
        tDiscovery = threading.Thread(target=threadDiscovery)
        tVmgr.start()
        # print('After VMGR: number of current threads is ', threading.active_count())
        # tAgent.start()
        # print('After Agent: number of current threads is ', threading.active_count())
        tAdvertisement.start()
        # print('After Advertisement: number of current threads is ', threading.active_count())
        tServer.start()
        # print('After Server: number of current threads is ', threading.active_count())
        tSWUpdate.start()
        tDiscovery.start()

    except KeyboardInterrupt:
        print('Starting Program Cleanup')