import eel
import threading

eel.init('gui-revised')
# my_options = {
#     'mode': "chrome", #or "chrome-app",
#     'host': 'localhost',
#     'port': 8080,
#     'chromeFlags': ["--start-fullscreen", "--browser-startup-dialog"]
# }
def startGUI():
    try:
        eel.start('index.html', mode=False)
    except (SystemExit, MemoryError, KeyboardInterrupt):
        pass
    print ('This is printed when the window is closed!')
    startGUI()

def publishBikeMode(mode):
    eel.updateBikeMode(mode.name)

def publishLeftTurnStatus(status):
    if status==True:
        eel.updateLeftTurnStatus(1)
    else:
        eel.updateLeftTurnStatus(0)

def publishRightTurnStatus(status):
    if status==True:
        eel.updateRightTurnStatus(1)
    else:
        eel.updateRightTurnStatus(0)

def publishSpeedPower(speed, power):
    eel.updateSpeedPower(speed, power)

def publishSOC(soc):
    eel.updateSOC(soc)

def startGUIThread():
    try:
        guiThread = threading.Thread(target=startGUI)
        guiThread.start()
    except:
        print("Error: Unable to start the GUI thread.")

@eel.expose
def rebootBoard():
    print('Rebooting the computer...')

@eel.expose
def startFastCharge():
    print('Starting Fast Charging')
