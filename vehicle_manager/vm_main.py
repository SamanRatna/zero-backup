import time
from gui import *
import threading
from event_handler import *
from gpio_manager import *
from vmgr_compute import *
from power_manager import *
from carbon_offset import CarbonOffsetCalculator
from quectel import *
import vehicle_states
from can_handler import *
from ble_agent import *
from ble_advertisement import *
from ble_gatt_server import *
from gps import *
from orientation import Orientation
from sw_update import *
from ble_adapter import *
from ble_devices import *
from rider_info import *
from internet import *
from telematics import *

def threadAgent():
    time.sleep(2)
    startAgent()

def threadAdvertisement():
    time.sleep(4)
    startAdvertisementThread()

def threadServer():
    time.sleep(6)
    startServer()
    vehicleEvents.bluetoothState('SERVICES_OFF')

def threadDiscovery():
    time.sleep(8)
    setDiscovery(True)

def threadOrientation():
    orientation = Orientation.getInstance()

def threadCANHandler():
    can = CANHandler()

def threadTelematics():
    telematics = Telematics()

def threadVehicleManager():
    startGUIThread()
    quectel = Quectel.getInstance()
    powerManager = PowerManager()
    # gpioWriter = GPIOWriter.getInstance()
    vmgrComputer = VehicleInfoCalculator()
    carbonOffsetCalculator = CarbonOffsetCalculator()

def threadSWUpdate():
    swupdate()

def main():
    try:
        tAgent = threading.Thread(target = threadAgent)
        tAdvertisement = threading.Thread(target = threadAdvertisement)
        tServer = threading.Thread(target = threadServer)
        tVmgr = threading.Thread(target = threadVehicleManager)
        tOrientation = threading.Thread(target = threadOrientation)
        tCAN = threading.Thread(target = threadCANHandler)
        tSWUpdate = threading.Thread(target=threadSWUpdate)
        tTelematics = threading.Thread(target=threadTelematics)
        tDiscovery = threading.Thread(target=threadDiscovery)
        tVmgr.start()
        tCAN.start()
        tOrientation.start()
        tTelematics.start()
        # # print('After VMGR: number of current threads is ', threading.active_count())
        tAgent.start()
        # # print('After Agent: number of current threads is ', threading.active_count())
        tAdvertisement.start()
        # # print('After Advertisement: number of current threads is ', threading.active_count())
        tServer.start()
        # # print('After Server: number of current threads is ', threading.active_count())
        # # tSWUpdate.start()
        # tDiscovery.start()

    except KeyboardInterrupt:
        print('Starting Program Cleanup')

if __name__ == '__main__':
    main()
