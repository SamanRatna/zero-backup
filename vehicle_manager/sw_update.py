#!/usr/bin/python3

import time
import zmq
from event_handler import *
import subprocess
import os,pwd, sys

def swupdate():
    
    print("starting software update listener")
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5559")

    #  Do some 'work'
    time.sleep(1)

    swupdate_dict = {
        'update_info': None,
        'update_checked':None
    }

    def check_update():

        current_SW = subprocess.getoutput("sudo mender -show-artifact")

        print("-----------------------------------------------------------------")
        print("current SW is")
        print(current_SW)

        # Get latest update_info from update_info_daemon.py script that is always running

        # connection to update_info_daemon.py
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        socket.connect("tcp://localhost:5533")

        # request for latest release name
        socket.send(b"Get me the new release name")
        print("-----------------------------------------------------------------")
        print("requesting new release info")

        # reply from update_info_daemon.py
        message = socket.recv_multipart()

        # the reply message is an array with 3 frames/elements, the 3rd frame contains the update_info
        update_name = message[2]

        # the message is in bytes datatype, therefore, decoding it to string
        new_update = update_name.decode()
        swupdate_dict['update_checked'] = new_update

        print("-----------------------------------------------------------------")
        print("New update release is ")
        print(new_update)
        print("-----------------------------------------------------------------")

        if (current_SW == new_update):

            # Update is not needed
            swupdate_dict['update_checked'] = "You are up to date !"
            vehicleEvents.swupdate(swupdate_dict['update_checked'])
            print("You are already up to date.")

        else:

            # Perform Update
            print("You got a new update ...")
            vehicleEvents.swupdate("You have got " + swupdate_dict['update_checked'])


    def swupdateResponse(response):

        # For successful update installation
        if(response == 0):

            print("-----------------------------------------------------------------")
            print("sending Exit status 0 to install ...")

            # send bytes 0 to the ArtifactInstall_02 script
            socket.send(b"0")

        # Condition for update check
        elif(response == "check"):

            print("-----------------------------------------------------------------")
            print("Checking for update ...")
            check_update()

        # For update cancellation
        elif(response == 1):
            
            # Cancellation needn't have to do anything
            print("-----------------------------------------------------------------")
            print("sending Exit Status 21 to cancel ...")

    # GUI to Python: name of the event: swupdateResponse
    # swupdateResponse event is subscribed here
    vehicleEvents.swupdateResponse += swupdateResponse

    # Receive update_info from ArtifactInstall_02
    update_info_bytes = socket.recv()
    print("Received request: %s" % update_info_bytes)
    swupdate_dict['update_info'] = update_info_bytes.decode()

    # Python to GUI: name of the event: swupdate
    vehicleEvents.swupdate(swupdate_dict['update_info'])


    











