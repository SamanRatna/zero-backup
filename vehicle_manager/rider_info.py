import json
from event_handler import *
import requests
from bike_credentials import *
from url import *
CREDENTIALS_FILE = "/etc/yatri/rider-info.json"

def getRiderInfo():
    try:
        with open(CREDENTIALS_FILE, "r") as f:
            info = json.load(f)
            vehicleReadings.riderInfo(info)
            print(info)
    except Exception as err:
        print(err)

def saveRiderInfo(name, licenseNumber, bikeNumber):
    info = {
        "Name" : name,
        "LicenseNumber": licenseNumber,
        "BikeNumber": bikeNumber
    }
    vehicleReadings.riderInfo(info)
    with open(CREDENTIALS_FILE, 'w') as f:  # writing JSON object
        json.dump(info, f)

def fetchInfo():
    try:
        # url = "http://yatri-embedded-env.eba-gpw9ppqj.ap-south-1.elasticbeanstalk.com/api/v1/bikes/user"
        payload={}
        response = requests.request("GET", URL_RIDER_INFO, headers=headerRiderInfo, data=payload)
        print(response.text)
        info = response.json()
        # print(info)
        # print(info['data']['user'])
        riderInfo = info['data']['user']
        name = '-'
        licenseNumber = '-'
        bikeNumber = '-'

        if 'name' in riderInfo:
            name = riderInfo['name']
        if 'licenseNumber' in riderInfo:
            licenseNumber = riderInfo['licenseNumber']
        if 'bikeNumber' in riderInfo:
            bikeNumber = riderInfo['bikeNumber']

        saveRiderInfo(name, licenseNumber, bikeNumber)
    except Exception as err:
        print(err)

vehicleEvents.guiReady += getRiderInfo
vehicleEvents.fetchRiderInfo += fetchInfo

if __name__ == "__main__":
    getRiderInfo()