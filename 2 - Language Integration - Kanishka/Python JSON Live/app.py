# Import stuff
from flask import Flask, render_template
from pusher import Pusher
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import requests
import json
import atexit
import time
# import plotly
# import plotly.graph_objs as go
import random

# Create Flask app
app = Flask(__name__)

# Activate Pusher
pusher = Pusher(
    app_id='791854',
    key='79949ba2731f8c34ad11',
    secret='8024d12a53d5eeac4aeb',
    cluster='ap2',
    ssl=True
)

# Define variables for data retrieval
x_data = []
y_data = []

# Render Flask
@app.route("/")
def index():
    return render_template("index.html")


def retrieve_data():
    x_data.append(time.strftime('%H:%M:%S'))
    y_data.append(random.random())
    if len(x_data) >= 100:
        # x_data.remove(1)
        # y_data.remove(1)
        del x_data[0]
        del y_data[0]
    data = {"x": x_data, "y": y_data}
    # with open('data.json', 'w') as file:
    #     json.dump(data, file, indent=2)
    pusher.trigger("random", "data-updated", data)


# create schedule for retrieving prices
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=retrieve_data,
    trigger=IntervalTrigger(seconds=0.5),
    id='prices_retrieval_job',
    name='Retrieve prices every .1 seconds',
    replace_existing=True,
    max_instances=10
)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

# run Flask app
app.run(debug=True, use_reloader=False)
