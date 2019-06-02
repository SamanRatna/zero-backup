import random
import json
import time

while True:
    # Create a random data point
    x_data = random.randint(1, 25)
    x_json = {'x': x_data}

    with open('x_data.json', 'w') as file:
        json.dump(x_json, file)

    time.sleep(.1)
