from datetime import datetime
from flask import Flask, render_template
from . import app

@app.route("/")
def home():
    return "Hello flask!"


@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content

# @app.route("/api/data")
# def get_data():
#     return app.send_static_file("data.json")