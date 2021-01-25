import http.client as httplib
from event_handler import *
def checkInternetConnectivity():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        # print('Internet Available')
        vehicleReadings.network({'internetConnectivity': True})
    except:
        conn.close()
        # print('Internet not Available')
        vehicleReadings.network({'internetConnectivity': False})

vehicleEvents.checkInternetConnectivity += checkInternetConnectivity

if __name__ == "__main__":
    print('Internet Connectivity Status: ', have_internet())