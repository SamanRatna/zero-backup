from events import Events

class VehicleEvents(Events):
    __events__ = ('onRUPress','onRDPress', 'onRBPress', 'onHibeamToggle', 'onRightSideLightToggle', 'onLeftSideLightToggle', 'onBrakeToggle', 'onStandSwitch', 'onIgnition')

vehicleEvents = VehicleEvents()