from event_handler import *
from gpio_manager import *
from state_manager import StateManager
from tail_light_controller import TailLightController
import vehicle_states
import threading
import time
from gui import *

startGUIThread()
stateMgr = StateManager.getInstance(GPIOWriter.getInstance())
tlContoller = TailLightController(GPIOWriter.getInstance())
gpioReader = GPIOReader.getInstance()
