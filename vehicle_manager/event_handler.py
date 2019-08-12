from events import Events

class VehicleEvents(Events):
    __events__ = ('onRUPress','onRDPress', 'onRBPress')

vehicleEvents = VehicleEvents()