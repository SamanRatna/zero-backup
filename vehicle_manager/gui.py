import eel
import threading
import multiprocessing
import os
import time
import netifaces
import logging
#Configure logger
logging.basicConfig(filename="charge.log", format = '%(asctime)s - %(levelname)s - %(message)s', filemode='w')
chargeLogger=logging.getLogger()
chargeLogger.setLevel(logging.WARNING)
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

# def publishLeftTurnStatus(status):
#     if status==True:
#         eel.updateLeftTurnStatus(1)
#     else:
#         eel.updateLeftTurnStatus(0)

# def publishRightTurnStatus(status):
#     if status==True:
#         eel.updateRightTurnStatus(1)
#     else:
#         eel.updateRightTurnStatus(0)

def publishSideLightStatus(status):
    eel.updateSideLight(status)

def publishBeamStatus(status):
    eel.updateBeam(status.name)

def publishSpeedPower(speed, power):
    eel.updateSpeedPower(speed, power)

def publishSOC(soc, rangeSuste, rangeThikka, rangeBabbal):
    eel.updateSOC(soc, rangeSuste, rangeThikka, rangeBabbal)

def publishOdometer(odometer):
    eel.updateOdometer(odometer)

def publishChargingStatus(status, current, timeToCharge):
    eel.updateChargingStatus(status, current, timeToCharge)

# def publishRange(rangeSuste, rangeThikka, rangeBabbal):
    # eel.updateRangeInKm(rangeSuste, rangeThikka, rangeBabbal)
    # pass
def startGUIThread():
    try:        
        guiThread = threading.Thread(target=startGUI)
        guiThread.start()
    except:
        print("Error: Unable to start the GUI thread.")

@eel.expose
def rebootBoard():
    print('Rebooting the computer...')
    os.system('sudo shutdown -h now')

@eel.expose
def startFastCharge(option):
    if(option == 0):
        print('Option Not available yet.')
        return;
    pFastCharge = multiprocessing.Process(target = fastCharge, args=(option,))
    pFastCharge.start()
    pFastCharge.join()
    print('Finished the charge process.')

def fastCharge(option):
    count = 1200*option
    while(count > 0):
        chargeLogger.warning('Sending')
        os.system('cansend can0 300#01E8034C04AA00')
        time.sleep(0.05)
        count = count - 1

@eel.expose
def getConnectivityStatus():
    print('Getting Connectivity Status')
    iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    ip = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
    eel.updateConnectivityStatus(iface, ip)