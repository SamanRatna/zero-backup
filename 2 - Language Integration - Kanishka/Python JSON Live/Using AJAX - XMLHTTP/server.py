# Import stuff
from flask import Flask, render_template

# Create Flask app
app = Flask(__name__)

# Render Flask
@app.route("/")
def index():
    return render_template("index.html")


# run Flask app
app.run(debug=True, use_reloader=False)
