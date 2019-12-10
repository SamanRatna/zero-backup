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

startGUIThread()
stateMgr = StateManager.getInstance(GPIOWriter.getInstance())
tlContoller = TailLightController(GPIOWriter.getInstance())
gpioReader = GPIOReader.getInstance()
cany = CANHandler(GPIOWriter.getInstance())
vmgrComputer = VehicleInfoCalculator()
