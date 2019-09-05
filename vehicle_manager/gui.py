import eel
import threading

eel.init('gui')

def startGUI():
    try:
        eel.start('index.html', cmdline_args=['--no-sandbox'])
    except (SystemExit, MemoryError, KeyboardInterrupt):
        pass
    print ('This is printed when the window is closed!')

def publishBikeMode(mode):
    eel.updateBikeMode(mode.name)

def startGUIThread():
    try:
        guiThread = threading.Thread(target=startGUI)
        guiThread.start()
    except:
        print("Error: Unable to start the GUI thread.")
