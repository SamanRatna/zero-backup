import json
from event_handler import *

CREDENTIALS_FILE = "credentials.json"


def getRiderInfo():
    try:
        with open(CREDENTIALS_FILE, "r") as f:
            info = json.load(f)
            vehicleReadings.riderInfo(info)
            print(info)
    except error as err:
        print(err)


vehicleEvents.guiReady += getRiderInfo

if __name__ == "__main__":
    getRiderInfo()