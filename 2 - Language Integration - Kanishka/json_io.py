from flask import Flask
app = Flask(__name__)

i = 1


@app.route('/')
def index():
    print(i)
    return 'Hello World'


if __name__ == "__main__":
    app.run(debug=True)
