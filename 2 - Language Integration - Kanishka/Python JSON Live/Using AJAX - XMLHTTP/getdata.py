import random
import json
import time

while True:
    # Start time counter
    start = time.time()

    # Create a random data point
    x_data = random.randint(1, 25)
    x_json = {'x': x_data}

    with open('x_data.json', 'w') as file:
        json.dump(x_json, file)

    time.sleep(.01)

    # End time counter and display time taken
    end = time.time()
    if end-start != 0:
        print('Time taken: ', end-start, ' seconds')
