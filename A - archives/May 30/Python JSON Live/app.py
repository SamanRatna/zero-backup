import json
import numpy as np

n_row = 2
n_column = 10

for i in range(10):
    array = np.random.rand(n_row, n_column)
    array = array.tolist()
    x_data = {"x": array[0]}
    y_data = {"y": array[1]}
    data = [x_data, y_data]
    # print(data)
    with open('data.json', 'w') as file_x:
        json.dump(data, file_x, indent=2)
