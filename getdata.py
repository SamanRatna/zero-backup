import random
import json
import time

while True:
    # Start time counter
    start = time.time()

    # Create a data set
    power = random.randint(1, 10)
    speed = random.randint(20, 30)
    rem_range = random.randint(80, 84)

    data_json = {
        'power': power,
        'speed': speed,
        'range': rem_range
    }

    with open('data.json', 'w') as file:
        json.dump(data_json, file)

    time.sleep(.02)

    # End time counter and display time taken
    end = time.time()
    if end-start != 0:
        print('Time taken: ', end-start, ' seconds')
