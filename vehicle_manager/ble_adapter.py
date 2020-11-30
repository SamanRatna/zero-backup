import dbus
 
# Create Python object from /org/freedesktop/NetworkManager instance
# in org.freedesktop.NetworkManager application.
# nm = bus.get_object(BUS_NAME, '/org/bluez/hci0')
# print(nm)
# Get list of active connections from the properties
# "Get" method is in "org.freedesktop.DBus.Properties" interface
# It takes the interface name which has the property and name of
# the property as arguments.

def setDiscovery(state):
    bus = dbus.SystemBus()
 
    # Warning: Bus names and interfaces are different terms.
    # Just because they contain same format or even same data
    # does not mean they are the same thing.
    # I used these variables to denote the diffrance where bus names and
    # interfaces are used.
    BUS_NAME = 'org.bluez'
    AGENT_INTERFACE = 'org.bluez.Adapter1'

    adapter_path = '/org/bluez/hci0'
    adapter = dbus.Interface(bus.get_object("org.bluez", adapter_path),
					"org.freedesktop.DBus.Properties")
    connections = adapter.Get(AGENT_INTERFACE, 'Discoverable',
                     dbus_interface=dbus.PROPERTIES_IFACE)
    # print(connections)

    adapter.Set(AGENT_INTERFACE, 'Discoverable', dbus.Boolean(state))
 