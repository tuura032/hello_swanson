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
    id = random.randint(1, 58)
    line = webapp.db.execute("select * from quotes where id = :id", \
        {"id": id}).fetchall()

    avg_rating = webapp.db.execute("select avg(rating) from quote_ratings where quote_id = :id", \
        {"id": id}).fetchone()

    

    quote_id = line[0][0]
    quote = line[0][1]
    word_count = line[0][2]
    avg_rating = avg_rating[0]
    print("average rating: ", end='')
    print(avg_rating)

    try:
        avg_rating = int(avg_rating)
        print(avg_rating)
    except:
        print("not an int")

        print(avg_rating)
    
    response = jsonify({
        "id": quote_id,
        "quote": quote,
        "word_count": word_count,
        "author": "Ron Swanson",
        "average_rating": avg_rating
    })

    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

@app.route("/api/<quote_size>")
def get_quote_sized(quote_size):

    # randomly get one quote from db filtered by size
    if quote_size == "large":
        line = webapp.db.execute("select * from quotes where id IN (select id from quotes where quote_length > 12) order by RANDOM() LIMIT 1").fetchone()
    elif quote_size == "medium":
        line = webapp.db.execute("select * from quotes where id IN (select id from quotes where quote_length < 13 and quote_length > 4) order by RANDOM() LIMIT 1").fetchone()
    elif quote_size == "small":
        line = webapp.db.execute("select * from quotes where id IN (select id from quotes where quote_length < 5) order by RANDOM() LIMIT 1").fetchone()
    else:
        return redirect("/")

    quote_id = line[0]
    quote = line[1]
    word_count = line[2]

    avg_rating = webapp.db.execute("selct * from quote_ratings where quote_id = :q and user_ip = :ip", \
            {"q": quote_id, "ip": user_ip}).fetchall()

    response = jsonify({
        "id": quote_id,
        "quote": quote,
        "word_count": word_count,
        "author": "Ron Swanson",
        "average_rating": avg_rating
    })

    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

@app.route("/api/rating", methods = ["GET", "POST"])
def rating():
    if request.method == "POST":
        
        # receive post request
        rating = request.get_json()["user_rating"]
        quote_id = request.get_json()["quote_id"]
        user_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        
        # check db to ensure unique
        # if webapp.db.execute("select * from quote_ratings where quote_id = :q and user_ip = :ip", \
        #     {"q": quote_id, "ip": user_ip}).fetchall():
        #     print("yup")
        
        try:
            webapp.db.execute("insert into quote_ratings(quote_id, rating, user_ip) values (:quote_id, :rating, :user_ip)", \
                {"quote_id": quote_id, "rating": rating, "user_ip": user_ip})
            webapp.db.commit()
        except:
            print("no worries, you already rated")
            return "Already rated this one"

        return "Nice work, rating went through!"