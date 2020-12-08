#!/usr/bin/python3

# Import libraries
import zmq

# Prepare our context and sockets
context = zmq.Context()
frontend = context.socket(zmq.ROUTER)
backend = context.socket(zmq.DEALER)
frontend.bind("tcp://*:5532")
backend.bind("tcp://*:5533")

# Initialize poll set
poller = zmq.Poller()
poller.register(frontend, zmq.POLLIN)
poller.register(backend, zmq.POLLIN)

new_update = bytearray()

# # Switch messages between sockets
while True:

    print("polling ...")

    # print("loop entered")
    socks = dict(poller.poll())

    # Message sent from ArtifactInstall_01 received here. Message contains release name
    if socks.get(frontend) == zmq.POLLIN:

        print("-----------------------------------------------------------------")
        print("Receiving release name from ArtifactInstall_01")
        message = frontend.recv_multipart()
        print(message)
        print("-----------------------------------------------------------------")
        frontend.send_multipart(message)

    # Request from check_update function of swupdate.py received here
    if socks.get(backend) == zmq.POLLIN:
        
        print("-----------------------------------------------------------------")
        message1 = backend.recv_multipart()
        print("Received request from check_update")

        backend.send_multipart(message)
        print("Sent this release name")
        print(message)
        print("-----------------------------------------------------------------")
            
