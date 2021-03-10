import json
FILE_MAPBOX = "/etc/mapbox/api.json"
def returnAPI():
    print('Returning API')
    value = '0'
    try:
        with open(FILE_MAPBOX, 'r') as f:
            api = json.load(f)
        value = api
    except Exception as error:
        print(error)
    return(value)
