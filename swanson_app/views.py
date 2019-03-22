from datetime import datetime
from flask import Flask, render_template, session, request, url_for, redirect, jsonify
import re
import random
from . import webapp
from . import app

@app.route("/")
def home():
    return render_template("index.html")


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

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

@app.route("/api/quote")
def get_quote():
    id = random.randint(1, 59)
    line = webapp.db.execute("select * from quotes where id = :id", \
        {"id": id}).fetchall()

    quote_id = line[0][0]
    quote = line[0][1]
    word_count = line[0][2]
    
    print(line[0][1])
    response = jsonify({
        "id": quote_id,
        "quote": quote,
        "word_count": word_count,
        "author": "Ron Swanson"
    })

    response.headers.add("Access-Control-Allow-Origin", "*")

    return response