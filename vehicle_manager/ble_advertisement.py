#!/usr/bin/python

from __future__ import print_function
import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service
from event_handler import *
import array
import threading
try:
  from gi.repository import GObject  # python3
except ImportError:
  import gobject as GObject  # python2

from random import randint
import json
bluetoothName = 'Yatri Appollo'
mainloop = None
devices = {}
BLUEZ_SERVICE_NAME = 'org.bluez'
LE_ADVERTISING_MANAGER_IFACE = 'org.bluez.LEAdvertisingManager1'
DBUS_OM_IFACE = 'org.freedesktop.DBus.ObjectManager'
DBUS_PROP_IFACE = 'org.freedesktop.DBus.Properties'

LE_ADVERTISEMENT_IFACE = 'org.bluez.LEAdvertisement1'


class InvalidArgsException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.freedesktop.DBus.Error.InvalidArgs'


class NotSupportedException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.NotSupported'


class NotPermittedException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.NotPermitted'


class InvalidValueLengthException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.InvalidValueLength'


class FailedException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.Failed'

devicesFound =[]
class Devices:
    def __init__(self):
        self.devices = {}
    def updateConnection(self, deviceHandle, connection):
        if not deviceHandle in self.devices:
            self.devices[deviceHandle] = { }
        
        self.devices[deviceHandle]["Connected"] = connection
        print('BLE_ADVERTISEMENT: updateConnection')
        print(self.devices)
        if 'Name' in self.devices[deviceHandle]:
            vehicleEvents.onBluetoothConnection(self.devices[deviceHandle]["Name"], self.devices[deviceHandle]["Connected"])
    def updateName(self, deviceHandle, name):
        self.devices[deviceHandle]["Name"] = name
        print('BLE_ADVERTISEMENT: updateName')
        print(self.devices)
        if 'Connected' in self.devices[deviceHandle]:
            vehicleEvents.onBluetoothConnection(self.devices[deviceHandle]["Name"], self.devices[deviceHandle]["Connected"])
    def updateAlias(self, deviceHandle, alias):
        self.devices[deviceHandle]["Alias"] = alias
        print('BLE_ADVERTISEMENT: updateAlias')
        print(self.devices)
    def updateTrust(self, deviceHandle, trust):
        self.devices[deviceHandle]["Trusted"] = trust
        print(self.devices)
    def updatePairing(self, deviceHandle, pairing):
        self.devices[deviceHandle]["Paired"] = pairing
        print(self.devices)
    def updateAddress(self, deviceHandle, address):
        self.devices[deviceHandle]["Address"] = address
        print(self.devices)
    def updateAddressType(self, deviceHandle, addressType):
        self.devices[deviceHandle]["AddressType"] = addressType
        print(self.devices)

bluetoothDevices = Devices()

class Advertisement(dbus.service.Object):
    PATH_BASE = '/org/bluez/example/advertisement'

    def __init__(self, bus, index, advertising_type):
        self.path = self.PATH_BASE + str(index)
        self.bus = bus
        self.ad_type = advertising_type
        self.service_uuids = None
        self.manufacturer_data = None
        self.solicit_uuids = None
        self.service_data = None
        self.local_name = None
        self.include_tx_power = None
        self.data = None
        dbus.service.Object.__init__(self, bus, self.path)

    def get_properties(self):
        properties = dict()
        properties['Type'] = self.ad_type
        if self.service_uuids is not None:
            properties['ServiceUUIDs'] = dbus.Array(self.service_uuids,
                                                    signature='s')
        if self.solicit_uuids is not None:
            properties['SolicitUUIDs'] = dbus.Array(self.solicit_uuids,
                                                    signature='s')
        if self.manufacturer_data is not None:
            properties['ManufacturerData'] = dbus.Dictionary(
                self.manufacturer_data, signature='qv')
        if self.service_data is not None:
            properties['ServiceData'] = dbus.Dictionary(self.service_data,
                                                        signature='sv')
        if self.local_name is not None:
            properties['LocalName'] = dbus.String(self.local_name)
        if self.include_tx_power is not None:
            properties['IncludeTxPower'] = dbus.Boolean(self.include_tx_power)

        if self.data is not None:
            properties['Data'] = dbus.Dictionary(
                self.data, signature='yv')
        return {LE_ADVERTISEMENT_IFACE: properties}

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_service_uuid(self, uuid):
        if not self.service_uuids:
            self.service_uuids = []
        self.service_uuids.append(uuid)

    def add_solicit_uuid(self, uuid):
        if not self.solicit_uuids:
            self.solicit_uuids = []
        self.solicit_uuids.append(uuid)

    def add_manufacturer_data(self, manuf_code, data):
        if not self.manufacturer_data:
            self.manufacturer_data = dbus.Dictionary({}, signature='qv')
        self.manufacturer_data[manuf_code] = dbus.Array(data, signature='y')

    def add_service_data(self, uuid, data):
        if not self.service_data:
            self.service_data = dbus.Dictionary({}, signature='sv')
        self.service_data[uuid] = dbus.Array(data, signature='y')

    def add_local_name(self, name):
        if not self.local_name:
            self.local_name = ""
        self.local_name = dbus.String(name)

    def add_data(self, ad_type, data):
        if not self.data:
            self.data = dbus.Dictionary({}, signature='yv')
        self.data[ad_type] = dbus.Array(data, signature='y')

    @dbus.service.method(DBUS_PROP_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface):
        print('GetAll')
        if interface != LE_ADVERTISEMENT_IFACE:
            raise InvalidArgsException()
        print('returning props')
        return self.get_properties()[LE_ADVERTISEMENT_IFACE]

    @dbus.service.method(LE_ADVERTISEMENT_IFACE,
                         in_signature='',
                         out_signature='')
    def Release(self):
        print('%s: Released!' % self.path)

class TestAdvertisement(Advertisement):

    def __init__(self, bus, index):
        global bluetoothName
        Advertisement.__init__(self, bus, index, 'peripheral')
        # self.add_service_uuid('180D')
        self.add_service_uuid('180F')
        self.add_manufacturer_data(0xffff, [0x00, 0x01, 0x02, 0x03, 0x04])
        self.add_service_data('9999', [0x00, 0x01, 0x02, 0x03, 0x04])
        self.add_local_name(bluetoothName)
        self.include_tx_power = True
        # self.add_data(0x26, [0x01, 0x01, 0x00])

def propertiesChangedCb(*args, **kwargs):
    global devices
    global bluetoothDevices
    dev = None
    if 'path' in kwargs:
        devPath = kwargs['path']
        print(devPath)
        print(str(devPath))
        strDevPath = str(devPath)
        devIntermediate = strDevPath.replace('/org/bluez/hci0/dev_','')
        dev=devIntermediate.replace('_',':')
        print(dev)

    for i, arg in enumerate(args):
        if(i==1):
            if 'Name' in arg:
                deviceName = str(arg['Name'])
                print("Device Name: ", deviceName)
                bluetoothDevices.updateName(dev, deviceName)

            if 'Connected' in arg:
                isConnected = bool(arg['Connected'])
                bluetoothDevices.updateConnection(dev, isConnected)

def interfacesAddedCb(*args, **kwargs):
    print('interfacesAddedCb')
    dev = None
    if 'path' in kwargs:
        devPath = kwargs['path']
        print(devPath)
        print(str(devPath))
        strDevPath = str(devPath)
        devIntermediate = strDevPath.replace('/org/bluez/hci0/dev_','')
        dev=devIntermediate.replace('_',':')
        print(dev)
    for i, arg in enumerate(args):
        if(i==1):
            if not 'org.bluez.Device1' in arg:
                print('org.bluez.Device1 key not found')
                return

            if 'Connected' in arg['org.bluez.Device1']:
                isConnected = bool(arg["org.bluez.Device1"]["Connected"])
                bluetoothDevices.updateConnection(dev, isConnected)

            if 'Paired' in arg['org.bluez.Device1']:
                isPaired = bool(arg["org.bluez.Device1"]["Paired"])
                bluetoothDevices.updatePairing(dev, isPaired)

            if 'Trusted' in arg['org.bluez.Device1']:
                isTrusted = bool(arg["org.bluez.Device1"]["Trusted"])
                bluetoothDevices.updateTrust(dev, isTrusted)

def register_ad_cb():
    global bluetoothName
    vehicleEvents.onBLEReady([2, bluetoothName])
    print('Advertisement registered')


def register_ad_error_cb(error):
    print('Failed to register advertisement: ' + str(error))
    mainloop.quit()


def find_adapter(bus):
    remote_om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'),
                               DBUS_OM_IFACE)
    objects = remote_om.GetManagedObjects()

    for o, props in objects.items():
        if LE_ADVERTISING_MANAGER_IFACE in props:
            return o

    return None

def find_devices(bus):
    global bluetoothDevices
    remote_om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'),
                               DBUS_OM_IFACE)
    objects = remote_om.GetManagedObjects()

    for o, props in objects.items():
        if "org.bluez.Device1" in props:
            print('Device Found.')
            device = {}
            if "Name" in props["org.bluez.Device1"]:
                device["Name"] = str(props["org.bluez.Device1"]["Name"])
            if "Alias" in props["org.bluez.Device1"]:
                device["Alias"] = str(props["org.bluez.Device1"]["Alias"])
            if "Address" in props["org.bluez.Device1"]:
                device["Address"] = str(props["org.bluez.Device1"]["Address"])
            if "Trusted" in props["org.bluez.Device1"]:
                device["Trusted"] = bool(props["org.bluez.Device1"]["Trusted"])
            if "Paired" in props["org.bluez.Device1"]:
                device["Paired"] = bool(props["org.bluez.Device1"]["Paired"])
            if "Connected" in props["org.bluez.Device1"]:
                device["Connected"] = bool(props["org.bluez.Device1"]["Connected"])
            # bluetoothDevices.devices["org.bluez.Device1"] = device
            bluetoothDevices.devices[device['Address']] = device
    print('Found the following devices:')
    print(bluetoothDevices.devices)
    global devicesFound
    for key in bluetoothDevices.devices:
        print(key, '->', bluetoothDevices.devices[key])
        devicesFound.append(bluetoothDevices.devices[key]['Alias'])
    vehicleReadings.bleDevices(devicesFound)
    # if 'org.bluez.Device1' in bluetoothDevices.devices:
    #     if('Name' in bluetoothDevices.devices['org.bluez.Device1']):
    #         print('Sending device list to UI: ', bluetoothDevices.devices['org.bluez.Device1']['Name'])
    #         vehicleReadings.bleDevices([bluetoothDevices.devices['org.bluez.Device1']['Name']])
    
    return

def startAdvertisement():
    getBluetoothNameFromPersistency()
    global mainloop

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()

    #register your signal callback
    bus.add_signal_receiver(propertiesChangedCb,
            dbus_interface = "org.freedesktop.DBus.Properties",
            signal_name = "PropertiesChanged",
            arg0 = "org.bluez.Device1",
            path_keyword = "path")
    
    bus.add_signal_receiver(interfacesAddedCb,
            dbus_interface = "org.freedesktop.DBus.ObjectManager",
            signal_name = "InterfacesAdded")

    adapter = find_adapter(bus)
    if not adapter:
        print('LEAdvertisingManager1 interface not found')
        return
    find_devices(bus)
    adapter_props = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, adapter),
                                   "org.freedesktop.DBus.Properties");

    adapter_props.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))

    ad_manager = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, adapter),
                                LE_ADVERTISING_MANAGER_IFACE)

    test_advertisement = TestAdvertisement(bus, 0)

    mainloop = GObject.MainLoop()

    ad_manager.RegisterAdvertisement(test_advertisement.get_path(), {},
                                     reply_handler=register_ad_cb,
                                     error_handler=register_ad_error_cb)

    mainloop.run()
    ad_manager.UnregisterAdvertisement(test_advertisement)
    print('Advertisement unregistered')
    dbus.service.Object.remove_from_connection(test_advertisement)
    vehicleEvents.onBLEReady([0, bluetoothName])

def quitAdvertisement():
    global mainloop
    mainloop.quit()

def enableBluetooth(toState):
    if (toState == True):
        startAdvertisementThread()
    else:
        quitAdvertisement()

def startAdvertisementThread():
    tAdvertisement = threading.Thread(target = startAdvertisement)
    tAdvertisement.start()
    # print('Started Advertisement Thread. Thread Count: ', threading.active_count())

def onGUIReady():
    global devicesFound
    vehicleEvents.onBLEReady([1, bluetoothName])
    vehicleReadings.bleDevices(devicesFound)

def onChangeBluetoothName(name):
    global bluetoothName
    bluetoothName = name
    saveBluetoothNameToPersistency()

def saveBluetoothNameToPersistency():
    global bluetoothName
    data = {'bluetooth-name' : bluetoothName}
    with open('bluetooth.json', 'w') as f:
        json.dump(data, f)

def getBluetoothNameFromPersistency():
    global bluetoothName
    try:
        with open('bluetooth.json', 'r') as f:
            data = json.load(f)
            if 'bluetooth-name' in data:
                bluetoothName = data['bluetooth-name']
    except Exception as error:
        print(error)
        return

vehicleEvents.guiReady += onGUIReady
vehicleEvents.onBluetooth += enableBluetooth
vehicleEvents.onBluetoothNameChange += onChangeBluetoothName

if __name__ == '__main__':
    startAdvertisement()
