import dbus
import dbus.mainloop.glib
from gi.repository import GLib
import bluezutils
from event_handler import *

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SystemBus()
mainloop = GLib.MainLoop()


def removeDevice(address):
	managed_objects = bluezutils.get_managed_objects()
	adapter = bluezutils.find_adapter_in_objects(managed_objects)
	try:
		dev = bluezutils.find_device_in_objects(managed_objects,
							address)
		path = dev.object_path
	except:
		path = address
	adapter.RemoveDevice(path)

def getDeviceList():
	deviceList = []
	manager = dbus.Interface(bus.get_object("org.bluez", "/"),
						"org.freedesktop.DBus.ObjectManager")
	
	objects = manager.GetManagedObjects()
	
	all_devices = (str(path) for path, interfaces in objects.items() if
						"org.bluez.Device1" in interfaces.keys())
	
	for path, interfaces in objects.items():
		device_list = [d for d in all_devices if d.startswith(path + "/")]
	
		for dev_path in device_list:
			# print("    [ " + dev_path + " ]")
	
			dev = objects[dev_path]
			properties = dev["org.bluez.Device1"]
			
			device = {}
			for key in properties.keys():
				value = properties[key]
				if(key == "Name"):
					device[str(key)] = str(value)
				if(key == "Alias"):
					device[str(key)] = str(value)
				if (key == "Address"):
					device[str(key)] = str(value)
				if(key == "Trusted"):
					device[str(key)] = bool(value)
				if(key == "Paired"):
					device[str(key)] = bool(value)
				if (key == "Connected"):
					device[str(key)] = bool(value)
			deviceList.append(device)
	return deviceList

def broadcastDeviceList():
	deviceList = getDeviceList()
	vehicleReadings.bleDevices(deviceList)

def removeAllDevices():
	deviceList = getDeviceList()
	if(len(deviceList) == 0):
		print('No devices found.')
		return
	
	print('-----------------------------------')
	print('Following bluetooth devices found:')
	for device in deviceList:
		print(device)
	print('-----------------------------------')

	for device in deviceList:
		if('Address' in device):
			removeDevice(device['Address'])
	
	broadcastDeviceList()

vehicleEvents.removeBluetoothDevices += removeAllDevices
vehicleEvents.guiReady += broadcastDeviceList
if __name__=='__main__':
	removeAllDevices()