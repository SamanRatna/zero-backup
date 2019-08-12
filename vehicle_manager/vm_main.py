from state_manager import StateManager
from gpio_manager import GPIOManager

if __name__ == '__main__':
    gpioMgr = GPIOManager('gpio_config.json')
    stateMgr = StateManager()
    while True:
        changes, input = gpioMgr.monitorGPIO()
        if changes.len() != 0:
            stateMgr.updateState(changes, input)
        sleep(0.1)