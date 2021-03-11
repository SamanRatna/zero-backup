import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import threading
from event_handler import *
import subprocess

DBusGMainLoop(set_as_default=True)

# signal handler to handle the changes in the property of BLE Adapter
def adapterSignalHandler(*args, **kwargs):
    data = args[1]
    if('Powered' in data):
        state = bool(data['Powered'])
        broadcastPoweredState(state)

    if('Discoverable' in data):
        state = bool(data['Discoverable'])
        broadcastDiscoverableState(state)

# emit the powered state of the BLE
def broadcastPoweredState(state):
    if(state):
        vehicleEvents.bluetoothStatus('POWERED_ON')
    else:
        vehicleEvents.bluetoothStatus('POWERED_OFF')

# emit the discoverable state of the BLE
def broadcastDiscoverableState(state):
    if(state):
        vehicleEvents.bluetoothStatus('DISCOVERABLE_ON')
    else:
        vehicleEvents.bluetoothStatus('DISCOVERABLE_OFF')

bus = dbus.SystemBus()
BUS_NAME = 'org.bluez'
ADAPTER_INTERFACE = 'org.bluez.Adapter1'
ADAPTER_PATH = '/org/bluez/hci0'
SIGNAL_NAME = 'PropertiesChanged'

# add the signal handler
bus.add_signal_receiver(adapterSignalHandler,
                        bus_name=BUS_NAME,
                        interface_keyword=ADAPTER_INTERFACE,
                        signal_name = SIGNAL_NAME,
                        path_keyword=ADAPTER_PATH
                        )

# subscribe to the dbus event loop
try:
    loop = GLib.MainLoop()
    loopThread = threading.Thread(target=loop.run)
    loopThread.start()
except Exception as e:
    print(e)

def getPoweredState():
    state = adapter.Get(ADAPTER_INTERFACE, "Powered")
    broadcastPoweredState(bool(state))

def getDiscoverableState():
    state = adapter.Get(ADAPTER_INTERFACE, "Discoverable")
    broadcastDiscoverableState(bool(state))

def setPoweredState(state):
    value = dbus.Boolean(state)
    adapter.Set("org.bluez.Adapter1", "Powered", value)

def setDiscoverableState(state):
    value = dbus.Boolean(state)
    adapter.Set("org.bluez.Adapter1", "Discoverable", value)

def setConnectableState(state):
    if(state):
        # process = subprocess.Popen('btmgmt connectable on; btmgmt discov on',stdout=subprocess.PIPE, shell=True)
        subprocess.call('btmgmt connectable on', shell=True)
    else:
        subprocess.call('btmgmt connectable off', shell=True)

def onGUIReady():
    getPoweredState()
    getDiscoverableState()

def monitorConnection(deviceName, connectionState):
    if(bool(int(connectionState))):
        setConnectableState(False)
    else:
        setConnectableState(True)
        setDiscoverableState(True)

def setBluetoothState(state):
    setPoweredState(state)
    if(state):
        setConnectableState(state)
        setDiscoverableState(state)
try:
    adapter = dbus.Interface(bus.get_object(BUS_NAME, ADAPTER_PATH), "org.freedesktop.DBus.Properties")

    # subscribe to events
    vehicleEvents.guiReady += onGUIReady
    vehicleEvents.onBluetooth += setBluetoothState
    # vehicleEvents.onBluetoothConnection += monitorConnection

except Exception as e:
    print(e)
