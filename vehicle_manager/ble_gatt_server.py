#!/usr/bin/env python3

import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service

from event_handler import *

import array
try:
  from gi.repository import GObject
except ImportError:
  import gobject as GObject
import sys

from random import randint

mainloop = None

BLUEZ_SERVICE_NAME = 'org.bluez'
GATT_MANAGER_IFACE = 'org.bluez.GattManager1'
DBUS_OM_IFACE =      'org.freedesktop.DBus.ObjectManager'
DBUS_PROP_IFACE =    'org.freedesktop.DBus.Properties'

GATT_SERVICE_IFACE = 'org.bluez.GattService1'
GATT_CHRC_IFACE =    'org.bluez.GattCharacteristic1'
GATT_DESC_IFACE =    'org.bluez.GattDescriptor1'

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

class Application(dbus.service.Object):
    """
    org.bluez.GattApplication1 interface implementation
    """
    def __init__(self, bus):
        self.path = '/'
        self.services = []
        dbus.service.Object.__init__(self, bus, self.path)
        self.add_service(BatteryService(bus, 0))
        self.add_service(VehicleManagerService(bus, 1))

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_service(self, service):
        self.services.append(service)

    @dbus.service.method(DBUS_OM_IFACE, out_signature='a{oa{sa{sv}}}')
    def GetManagedObjects(self):
        response = {}
        print('GetManagedObjects')

        for service in self.services:
            response[service.get_path()] = service.get_properties()
            chrcs = service.get_characteristics()
            for chrc in chrcs:
                response[chrc.get_path()] = chrc.get_properties()
                descs = chrc.get_descriptors()
                for desc in descs:
                    response[desc.get_path()] = desc.get_properties()

        return response


class Service(dbus.service.Object):
    """
    org.bluez.GattService1 interface implementation
    """
    PATH_BASE = '/org/bluez/example/service'

    def __init__(self, bus, index, uuid, primary):
        self.path = self.PATH_BASE + str(index)
        self.bus = bus
        self.uuid = uuid
        self.primary = primary
        self.characteristics = []
        dbus.service.Object.__init__(self, bus, self.path)

    def get_properties(self):
        return {
                GATT_SERVICE_IFACE: {
                        'UUID': self.uuid,
                        'Primary': self.primary,
                        'Characteristics': dbus.Array(
                                self.get_characteristic_paths(),
                                signature='o')
                }
        }

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_characteristic(self, characteristic):
        self.characteristics.append(characteristic)

    def get_characteristic_paths(self):
        result = []
        for chrc in self.characteristics:
            result.append(chrc.get_path())
        return result

    def get_characteristics(self):
        return self.characteristics

    @dbus.service.method(DBUS_PROP_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface):
        if interface != GATT_SERVICE_IFACE:
            raise InvalidArgsException()

        return self.get_properties()[GATT_SERVICE_IFACE]


class Characteristic(dbus.service.Object):
    """
    org.bluez.GattCharacteristic1 interface implementation
    """
    def __init__(self, bus, index, uuid, flags, service):
        self.path = service.path + '/char' + str(index)
        self.bus = bus
        self.uuid = uuid
        self.service = service
        self.flags = flags
        self.descriptors = []
        dbus.service.Object.__init__(self, bus, self.path)

    def get_properties(self):
        return {
                GATT_CHRC_IFACE: {
                        'Service': self.service.get_path(),
                        'UUID': self.uuid,
                        'Flags': self.flags,
                        'Descriptors': dbus.Array(
                                self.get_descriptor_paths(),
                                signature='o')
                }
        }

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_descriptor(self, descriptor):
        self.descriptors.append(descriptor)

    def get_descriptor_paths(self):
        result = []
        for desc in self.descriptors:
            result.append(desc.get_path())
        return result

    def get_descriptors(self):
        return self.descriptors

    @dbus.service.method(DBUS_PROP_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface):
        if interface != GATT_CHRC_IFACE:
            raise InvalidArgsException()

        return self.get_properties()[GATT_CHRC_IFACE]

    @dbus.service.method(GATT_CHRC_IFACE,
                        in_signature='a{sv}',
                        out_signature='ay')
    def ReadValue(self, options):
        print('Default ReadValue called, returning error')
        raise NotSupportedException()

    @dbus.service.method(GATT_CHRC_IFACE, in_signature='aya{sv}')
    def WriteValue(self, value, options):
        print('Default WriteValue called, returning error')
        raise NotSupportedException()

    @dbus.service.method(GATT_CHRC_IFACE)
    def StartNotify(self):
        print('Default StartNotify called, returning error')
        raise NotSupportedException()

    @dbus.service.method(GATT_CHRC_IFACE)
    def StopNotify(self):
        print('Default StopNotify called, returning error')
        raise NotSupportedException()

    @dbus.service.signal(DBUS_PROP_IFACE,
                         signature='sa{sv}as')
    def PropertiesChanged(self, interface, changed, invalidated):
        pass


class Descriptor(dbus.service.Object):
    """
    org.bluez.GattDescriptor1 interface implementation
    """
    def __init__(self, bus, index, uuid, flags, characteristic):
        self.path = characteristic.path + '/desc' + str(index)
        self.bus = bus
        self.uuid = uuid
        self.flags = flags
        self.chrc = characteristic
        dbus.service.Object.__init__(self, bus, self.path)

    def get_properties(self):
        return {
                GATT_DESC_IFACE: {
                        'Characteristic': self.chrc.get_path(),
                        'UUID': self.uuid,
                        'Flags': self.flags,
                }
        }

    def get_path(self):
        return dbus.ObjectPath(self.path)

    @dbus.service.method(DBUS_PROP_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface):
        if interface != GATT_DESC_IFACE:
            raise InvalidArgsException()

        return self.get_properties()[GATT_DESC_IFACE]

    @dbus.service.method(GATT_DESC_IFACE,
                        in_signature='a{sv}',
                        out_signature='ay')
    def ReadValue(self, options):
        print ('Default ReadValue called, returning error')
        raise NotSupportedException()

    @dbus.service.method(GATT_DESC_IFACE, in_signature='aya{sv}')
    def WriteValue(self, value, options):
        print('Default WriteValue called, returning error')
        raise NotSupportedException()

''' -------------------------------------------------------------------------- '''
''' ----------------------- Battery Service ---------------------------------- '''
''' -------------------------------------------------------------------------- '''

class BatteryService(Service):
    BATTERY_UUID = '180f'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.BATTERY_UUID, True)
        self.add_characteristic(BatteryLevelCharacteristic(bus, 0, self))


class BatteryLevelCharacteristic(Characteristic):
    BATTERY_LVL_UUID = '2a19'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
                self, bus, index,
                self.BATTERY_LVL_UUID,
                ['encrypt-read', 'notify'],
                service)
        self.notifying = False
        self.battery_lvl = 100
        vehicleReadings.batteryStatus += self.actualBatteryLevel
        # GObject.timeout_add(5000, self.drain_battery)

    def notify_battery_level(self):
        if not self.notifying:
            return
        self.PropertiesChanged(
                GATT_CHRC_IFACE,
                { 'Value': [dbus.Byte(self.battery_lvl)] }, [])

    def drain_battery(self):
        if not self.notifying:
            return True
        if self.battery_lvl > 0:
            self.battery_lvl -= 2
            if self.battery_lvl < 0:
                self.battery_lvl = 0
        print('Battery Level drained: ' + repr(self.battery_lvl))
        self.notify_battery_level()
        return True
            # if self.battery_lvl > 0:
            #     self.battery_lvl -= 2
            # if self.battery_lvl <= 0:
            #     self.battery_lvl = 100
            # print('Battery Level drained: ' + repr(self.battery_lvl))
            # return True

    def actualBatteryLevel(self, value):
        self.battery_lvl = value        
        print('Battery Level received: ' + repr(self.battery_lvl))
        self.notify_battery_level()
        return True

    def ReadValue(self, options):
        print('Battery Level read: ' + repr(self.battery_lvl))
        return [dbus.Byte(self.battery_lvl)]

    def StartNotify(self):
        if self.notifying:
            print('Already notifying, nothing to do')
            return

        self.notifying = True
        self.notify_battery_level()

    def StopNotify(self):
        if not self.notifying:
            print('Not notifying, nothing to do')
            return

        self.notifying = False


''' -------------------------------------------------------------------------- '''
''' ----------------------- Vehicle Manager service -------------------------- '''
''' -------------------------------------------------------------------------- '''

class VehicleManagerService(Service):
    TEST_SVC_UUID = '2cc83522-8192-4b6c-ad94-1f54123ed820'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.TEST_SVC_UUID, True)
        self.add_characteristic(MaxSpeedCharacteristic(bus, 0, self))
        self.add_characteristic(AverageSpeedsCharacteristic(bus, 1, self))
        self.add_characteristic(TravelledDistancesCharacteristic(bus, 2, self))
        self.add_characteristic(VehicleFinderCharacteristic(bus, 3, self))
        self.add_characteristic(CarbonOffsetCharacteristic(bus, 4, self))

''' -------------------------------------------------------------------------- '''
''' ----------------------- Max Speed Characteristic ------------------------- '''
''' -------------------------------------------------------------------------- '''

class MaxSpeedCharacteristic(Characteristic):
    TEST_CHRC_UUID = '2cc83522-8192-4b6c-ad94-1f54123ed821'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
                self, bus, index,
                self.TEST_CHRC_UUID,
                ['encrypt-read', 'notify'],
                service)
        self.notifying = False
        self.maxSpeed = 0
        self.tripMaxSpeed = 0
        vehicleReadings.maxSpeed += self.SetMaxSpeed
        vehicleReadings.tripMaxSpeed += self.SetTripMaxSpeed
        self.add_descriptor(MaxSpeedDescriptor(bus, 0, self))
        # self.add_descriptor(
        #         CharacteristicUserDescriptionDescriptor(bus, 1, self))
        # GObject.timeout_add(5000, self.changeMaxSpeed)

    def SetMaxSpeed(self, speed):
        self.maxSpeed = speed
        print('BLE_GATT: Received Max Speed: ' + repr(self.maxSpeed))
        self.NotifyValue()
    
    def SetTripMaxSpeed(self, speed):
        self.tripMaxSpeed = speed
        print('BLE_GATT: Received Trip Max Speed: ' + repr(self.tripMaxSpeed))
        self.NotifyValue()

    def ReadValue(self, options):
        print('Max Speed Read: ' + repr(self.maxSpeed))
        return [dbus.Byte(self.maxSpeed), dbus.Byte(self.tripMaxSpeed)]

    def NotifyValue(self):
        if not self.notifying:
            return
        self.PropertiesChanged(
                GATT_CHRC_IFACE,
                { 'Value': [dbus.Byte(self.maxSpeed), dbus.Byte(self.tripMaxSpeed)] }, [])
    
    def StartNotify(self):
        if self.notifying:
            print('Already notifying, nothing to do')
            return

        self.notifying = True
        self.NotifyValue()

    def StopNotify(self):
        if not self.notifying:
            print('Not notifying, nothing to do')
            return

        self.notifying = False
    
    def changeMaxSpeed(self):
        if not self.notifying:
            return True
        if self.maxSpeed > 0:
            self.maxSpeed -= 2
            if self.maxSpeed < 0:
                self.maxSpeed = 0
        print('Max Speed Changed: ' + repr(self.maxSpeed))
        self.NotifyValue()
        return True

class MaxSpeedDescriptor(Descriptor):
    TEST_DESC_UUID = '2cc83522-8192-4b6c-ad94-1f54123ed822'

    def __init__(self, bus, index, characteristic):
        self.value = array.array('B', b'Maximum Speed of the vehicle in km/hr.')
        self.value = self.value.tolist()
        Descriptor.__init__(
                self, bus, index,
                self.TEST_DESC_UUID,
                ['read', 'write'],
                characteristic)

    def ReadValue(self, options):
        return self.value
''' -------------------------------------------------------------------------- '''
''' ------------------- Average Speed Characteristic ------------------------- '''
''' -------------------------------------------------------------------------- '''

# Average Speeds: Overall average speed and Trip average speed
class AverageSpeedsCharacteristic(Characteristic):
    AVSPEED_CHRC_UUID = '2cc83522-8192-4b6c-ad94-1f54123ed825'
    def __init__(self, bus, index, service):
        Characteristic.__init__(
                self, bus, index,
                self.AVSPEED_CHRC_UUID,
                ['encrypt-read', 'notify'],
                service)
        self.notifying = False
        self.tripAverageSpeed = 0
        self.totalAverageSpeed = 0
        vehicleReadings.averageSpeeds += self.SetAverageSpeeds
        self.add_descriptor(AverageSpeedsDescriptor(bus, 0, self))
        # self.add_descriptor(
        #         CharacteristicUserDescriptionDescriptor(bus, 1, self))
        # GObject.timeout_add(5000, self.changeSpeeds)
    def SetAverageSpeeds(self, odoAverage, tripAverage):
        self.tripAverageSpeed = int(tripAverage)
        self.totalAverageSpeed = int(odoAverage)
        print('BLE_GATT: Received Average Speeds: ' + repr(self.tripAverageSpeed), repr(self.totalAverageSpeed))
        self.NotifyValue()

    def ReadValue(self, options):
        print('Trip Average Speed Read: ' + repr(self.tripAverageSpeed))
        return [dbus.Byte(self.tripAverageSpeed), dbus.Byte(self.totalAverageSpeed)]

    def NotifyValue(self):
        if not self.notifying:
            return
        self.PropertiesChanged(
                GATT_CHRC_IFACE,
                { 'Value': [dbus.Byte(self.tripAverageSpeed), dbus.Byte(self.totalAverageSpeed)] }, [])
    
    def StartNotify(self):
        if self.notifying:
            print('Already notifying, nothing to do')
            return

        self.notifying = True
        self.NotifyValue()

    def StopNotify(self):
        if not self.notifying:
            print('Not notifying, nothing to do')
            return

        self.notifying = False
    
    def changeSpeeds(self):
        if not self.notifying:
            return True
        if self.tripAverageSpeed > 0:
            self.tripAverageSpeed -= 2
            if self.tripAverageSpeed < 0:
                self.tripAverageSpeed += 4
        if self.totalAverageSpeed > 0:
            self.totalAverageSpeed -= 2
            if self.totalAverageSpeed < 0:
                self.totalAverageSpeed += 4
        print('Average Speeds Changed: ' + repr(self.tripAverageSpeed), repr(self.totalAverageSpeed))
        self.NotifyValue()
        return True

class AverageSpeedsDescriptor(Descriptor):
    TEST_DESC_UUID = '2cc83522-8192-4b6c-ad94-1f54123ed826'

    def __init__(self, bus, index, characteristic):
        self.value = array.array('B', b'Trip Average Speed and Overall Average Speed of the vehicle in km/hr.')
        self.value = self.value.tolist()
        Descriptor.__init__(
                self, bus, index,
                self.TEST_DESC_UUID,
                ['read', 'write'],
                characteristic)

    def ReadValue(self, options):
        return self.value

''' -------------------------------------------------------------------------- '''
''' ------------------- Travelled Distances Characteristic ------------------- '''
''' -------------------------------------------------------------------------- '''

class TravelledDistancesCharacteristic(Characteristic):
    TEST_CHRC_UUID = '2cc83522-8192-4b6c-ad94-1f54123ed827'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
                self, bus, index,
                self.TEST_CHRC_UUID,
                ['encrypt-read', 'notify'],
                service)
        self.notifying = False
        self.tripDistance = 0
        self.totalDistance = 0
        vehicleReadings.distances += self.SetDistances
        self.add_descriptor(TravelledDistancesDescriptor(bus, 1, self))
        # self.add_descriptor(
        #         CharacteristicUserDescriptionDescriptor(bus, 1, self))
        # GObject.timeout_add(5000, self.changeDistances)
    def SetDistances(self, odoDistance, tripDistance):
        # tripDistance and odoDistance are floats so convert to integers
        self.tripDistance = int(tripDistance) 
        self.totalDistance = int(odoDistance)
        print('BLE_GATT: Travelled Distances: ' + repr(self.tripDistance), repr(self.totalDistance))
        self.NotifyValue()

    def ReadValue(self, options):
        print('Trip Distance Read: ' + repr(self.tripDistance))
        print('Total Distance Read: ' + repr(self.totalDistance))
        tripDistanceBytes = bytearray(self.tripDistance.to_bytes(4, byteorder='little'))
        totalDistanceBytes = bytearray(self.totalDistance.to_bytes(4, byteorder='little'))
        return [dbus.Byte(tripDistanceBytes[0]), dbus.Byte(tripDistanceBytes[1]), dbus.Byte(tripDistanceBytes[2]), dbus.Byte(tripDistanceBytes[3]), dbus.Byte(totalDistanceBytes[0]), dbus.Byte(totalDistanceBytes[1]), dbus.Byte(totalDistanceBytes[2]), dbus.Byte(totalDistanceBytes[3])]

    def NotifyValue(self):
        if not self.notifying:
            return
        tripDistanceBytes = bytearray(self.tripDistance.to_bytes(4, byteorder='little'))
        totalDistanceBytes = bytearray(self.totalDistance.to_bytes(4, byteorder='little'))
        self.PropertiesChanged(
                GATT_CHRC_IFACE,
                { 'Value': [dbus.Byte(tripDistanceBytes[0]), dbus.Byte(tripDistanceBytes[1]), dbus.Byte(tripDistanceBytes[2]), dbus.Byte(tripDistanceBytes[3]), dbus.Byte(totalDistanceBytes[0]), dbus.Byte(totalDistanceBytes[1]), dbus.Byte(totalDistanceBytes[2]), dbus.Byte(totalDistanceBytes[3])] }, [])
    
    def StartNotify(self):
        if self.notifying:
            print('Already notifying, nothing to do')
            return

        self.notifying = True
        self.NotifyValue()

    def StopNotify(self):
        if not self.notifying:
            print('Not notifying, nothing to do')
            return

        self.notifying = False
    
    def changeDistances(self):
        if not self.notifying:
            return True
        if self.tripDistance > 0:
            self.tripDistance -= 2
            if self.tripDistance < 0:
                self.tripDistance += 4
        if self.totalDistance > 0:
            self.totalDistance -= 2
            if self.totalDistance < 0:
                self.totalDistance += 4
        print('Distances Changed: ' + repr(self.tripDistance), repr(self.totalDistance))
        self.NotifyValue()
        return True

class TravelledDistancesDescriptor(Descriptor):
    TEST_DESC_UUID = '2cc83522-8192-4b6c-ad94-1f54123ed828'

    def __init__(self, bus, index, characteristic):
        self.value = array.array('B', b'Trip distance and Total distance travelled in km.')
        self.value = self.value.tolist()
        Descriptor.__init__(
                self, bus, index,
                self.TEST_DESC_UUID,
                ['read', 'write'],
                characteristic)

    def ReadValue(self, options):
        return self.value

class CharacteristicUserDescriptionDescriptor(Descriptor):
    """
    Writable CUD descriptor.

    """
    CUD_UUID = '2901'

    def __init__(self, bus, index, characteristic):
        self.writable = 'writable-auxiliaries' in characteristic.flags
        self.value = array.array('B', b'This is a characteristic for testing')
        self.value = self.value.tolist()
        Descriptor.__init__(
                self, bus, index,
                self.CUD_UUID,
                ['read', 'write'],
                characteristic)

    def ReadValue(self, options):
        return self.value

    def WriteValue(self, value, options):
        if not self.writable:
            raise NotPermittedException()
        self.value = value

''' -------------------------------------------------------------------------- '''
''' ------------------- Vehicle Finder Characteristic ------------------------ '''
''' -------------------------------------------------------------------------- '''

class VehicleFinderCharacteristic(Characteristic):
    TEST_CHRC_UUID = '2cc83522-8192-4b6c-ad94-1f54123ed829'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
                self, bus, index,
                self.TEST_CHRC_UUID,
                ['encrypt-write'],
                service)

        self.add_descriptor(VehicleFinderDescriptor(bus, 0, self))

    def WriteValue(self, value, options):
        print('TestCharacteristic Write: ' + repr(value))
        command = ''.join([str(v) for v in value])
        vehicleEvents.finder(command)

class VehicleFinderDescriptor(Descriptor):
    TEST_DESC_UUID = '2cc83522-8192-4b6c-ad94-1f54123ed830'

    def __init__(self, bus, index, characteristic):
        self.value = array.array('B', b'Vehicle Finder Characteristics.')
        self.value = self.value.tolist()
        Descriptor.__init__(
                self, bus, index,
                self.TEST_DESC_UUID,
                ['read', 'write'],
                characteristic)

    def ReadValue(self, options):
        return self.value

''' -------------------------------------------------------------------------- '''
''' ------------------- Carbon Offset Characteristic ------------------------- '''
''' -------------------------------------------------------------------------- '''

class CarbonOffsetCharacteristic(Characteristic):
    TEST_CHRC_UUID = '2cc83522-8192-4b6c-ad94-1f54123ed831'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
                self, bus, index,
                self.TEST_CHRC_UUID,
                ['encrypt-write', 'notify'],
                service)
        self.notifying = False
        self.date = ''
        self.carbonOffsetData = []
        vehicleReadings.carbonOffsetForBluetooth += self.onCarbonOffsetData
        self.add_descriptor(CarbonOffsetDescriptor(bus, 0, self))
        # self.add_descriptor(
        #         CharacteristicUserDescriptionDescriptor(bus, 1, self))

    def WriteValue(self, value, options):
        # print('TestCharacteristic Write: ' + repr(value))
        date = ''
        for v in value:
            date += str(v)
        self.date = date
        print('BLEGATT: Carbon Offset Date: ', date)
        vehicleEvents.onCarbonOffsetRequest(date)

    def NotifyValue(self):
        if not self.notifying:
            return

        for data in self.carbonOffsetData:
            dateBytes = bytearray(data[0], 'utf-8')
            dataBytes = bytearray(str(data[1]), 'utf-8')
            dbusBytes = []
            for v in list(dateBytes):
                dbusBytes.append(dbus.Byte(v))
            dbusBytes.append(dbus.Byte(bytes(':', 'utf-8')[0]))
            for v in list(dataBytes):
                dbusBytes.append(dbus.Byte(v))
            print(data)
            # print(dbusBytes)
            self.PropertiesChanged(
                    GATT_CHRC_IFACE,
                    { 'Value': dbus.Array(dbusBytes) }, [])

    def StartNotify(self):
        if self.notifying:
            print('Already notifying, nothing to do')
            return

        self.notifying = True
        self.NotifyValue()

    def StopNotify(self):
        if not self.notifying:
            print('Not notifying, nothing to do')
            return

        self.notifying = False

    def onCarbonOffsetData(self, data):
        self.carbonOffsetData = data
        print('Received Carbon Offset Data')
        print(self.carbonOffsetData)
        self.NotifyValue()

class CarbonOffsetDescriptor(Descriptor):
    TEST_DESC_UUID = '2cc83522-8192-4b6c-ad94-1f54123ed832'

    def __init__(self, bus, index, characteristic):
        self.value = array.array('B', b'Carbon Offset Data')
        self.value = self.value.tolist()
        Descriptor.__init__(
                self, bus, index,
                self.TEST_DESC_UUID,
                ['read', 'write'],
                characteristic)

    def ReadValue(self, options):
        return self.value

def register_app_cb():
    print('GATT application registered')
    vehicleEvents.onBLEReady([1])


def register_app_error_cb(error):
    print('Failed to register application: ' + str(error))
    mainloop.quit()


def find_adapter(bus):
    remote_om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'),
                               DBUS_OM_IFACE)
    objects = remote_om.GetManagedObjects()

    for o, props in objects.items():
        if GATT_MANAGER_IFACE in props.keys():
            return o

    return None


def startServer():
    global mainloop

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()

    adapter = find_adapter(bus)
    if not adapter:
        print('GattManager1 interface not found')
        return

    service_manager = dbus.Interface(
            bus.get_object(BLUEZ_SERVICE_NAME, adapter),
            GATT_MANAGER_IFACE)

    app = Application(bus)

    mainloop = GObject.MainLoop()

    print('Registering GATT application...')

    service_manager.RegisterApplication(app.get_path(), {},
                                    reply_handler=register_app_cb,
                                    error_handler=register_app_error_cb)

    mainloop.run()

if __name__ == '__main__':
    startServer()
