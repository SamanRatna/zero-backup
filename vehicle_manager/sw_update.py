#!/usr/bin/python3

import time
import zmq
from event_handler import *

import os,pwd, sys
# import tkinter, tkinter.messagebox

def swupdate():
    print("starting software update listener")
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5559")

    #while True:
    #  Wait for next request from client
    

    #  Do some 'work'
    time.sleep(1)

    def swupdateResponse(response):
        if(response == True):
            socket.send(b"0")
        else:
            socket.send(b"21")

    vehicleEvents.swupdateResponse += swupdateResponse

    message1 = socket.recv()
    print("Received request: %s" % message1)
    message = str(message1)

    vehicleEvents.swupdate(message)

    # socket.send(b"0")



# tkinter.sys.exit(0)

#  Send reply back to client
# socket.send(b"Yesssss")

# os.environ["DISPLAY"] = ":0"

# pwstruct = pwd.getpwnam("pi")
# os.setgid(pwstruct.pw_uid)
# os.setuid(pwstruct.pw_gid)

# window = tkinter.Tk()
# window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
# window.withdraw()

# if tkinter.messagebox.askyesno(message, 'Do you want to update to the latest release version?', icon='warning') == True:
    
#     print(0)
#     socket.send(b"0")
#     tkinter.sys.exit(0)

# else:
#     print(21)
#     socket.send(b"21")
#     os.execv(__file__, *sys.argv)
#     tkinter.sys.exit(21)
    

# window.deiconify()
# window.destroy()
# window.quit()




