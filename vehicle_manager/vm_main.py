from event_handler import *

from state_manager import StateManager
import vehicle_states

"""
def onRUPressEvent():
    print(5)
RUPressEvent = Events()
RUPressEvent.on_change += onRUPressEvent
RUPressEvent.on_change()
"""
#eventHandle = EventHandler.getInstance()
stateMgr = StateManager.getInstance()
vehicleEvents.onRUPress()