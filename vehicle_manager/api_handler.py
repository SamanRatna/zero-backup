import json

def returnAPI():
    print('Returning API')
    value = '0'
    try:
        with open('./test/maps-api.json', 'r') as f:
            api = json.load(f)
        value = api
    except ( ) as error:
        print(error)
    return(value)
