from events import Events

class VehicleEvents(Events):
    __events__ = ('onRUPress','onRDPress', 'onRDHold', 'onRBPress', 'onHibeamToggle', 'onRightSideLightToggle', 'onLeftSideLightToggle', 'onBrakeToggle', 'onStandSwitch', 'onIgnition', 'onCharging', 'onTripReset')

vehicleEvents = VehicleEvents()


def eventRUPress():
    print("RU Press Event Triggered.")

def eventRBPress():
    print("RB Press Event Triggered.")

def eventRDPress():
    print("RD Press Event Triggered.")

def eventRDHold():
    print("RD Hold Event Triggered.")

def eventLeftTurn(value):
    print("Left Turn Toggled: ", str(value))

def eventRightTurn(value):
    print("Right Turn Toggled: ", str(value))

def eventStand(state):
    print("Stand Toggled: " + str(state) )

def eventBrake(state):
    print("Brake Toggled: " + str(state))

def eventHibeam(state):
    print("Hibeam toggled: " + str(state))

def eventTripReset():
    print("Trip Reset Requested")

vehicleEvents.onRUPress += eventRUPress
vehicleEvents.onRBPress += eventRBPress
vehicleEvents.onRDPress += eventRDPress
vehicleEvents.onHibeamToggle += eventHibeam
vehicleEvents.onRightSideLightToggle += eventRightTurn
vehicleEvents.onLeftSideLightToggle += eventLeftTurn
vehicleEvents.onBrakeToggle += eventBrake
vehicleEvents.onStandSwitch += eventStand
vehicleEvents.onRDHold += eventRDHold
vehicleEvents.onTripReset += eventTripReset