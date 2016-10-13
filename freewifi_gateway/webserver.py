from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


def do_start():
    app.run()
