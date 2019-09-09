import eel
import threading

eel.init('gui')

def startGUI():
    try:
        eel.start('index.html', cmdline_args=['--no-sandbox'])
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

def startGUIThread():
    try:
        guiThread = threading.Thread(target=startGUI)
        guiThread.start()
    except:
        print("Error: Unable to start the GUI thread.")
