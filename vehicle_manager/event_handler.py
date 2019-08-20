from events import Events

class VehicleEvents(Events):
    __events__ = ('onRUPress','onRDPress', 'onRBPress', 'onHibeamToggle', 'onRightSideLightToggle', 'onLeftSideLightToggle', 'onBrakeToggle', 'onStandSwitch', 'onIgnition', 'onCharging')

vehicleEvents = VehicleEvents()


def eventRUPress():
    print("RU Press Event Triggered.")

def eventRBPress():
    print("RB Press Event Triggered.")

def eventRDPress():
    print("RD Press Event Triggered.")

def eventLeftTurn():
    print("Left Turn Toggled")

def eventRightTurn():
    print("Right Turn Toggled")

def eventStand(state):
    print("Stand Toggled: " + str(state))

def eventBrake(state):
    print("Brake Toggled: " + str(state))

def eventHibeam(state):
    print("Hibeam toggled: " + str(state))

vehicleEvents.onRUPress += eventRUPress
vehicleEvents.onRBPress += eventRBPress
vehicleEvents.onRDPress += eventRDPress
vehicleEvents.onHibeamToggle += eventHibeam
vehicleEvents.onRightSideLightToggle += eventRightTurn
vehicleEvents.onLeftSideLightToggle += eventLeftTurn
vehicleEvents.onBrakeToggle += eventBrake
vehicleEvents.onStandSwitch += eventSwitch

