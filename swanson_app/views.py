from flask import Flask, render_template, session, request, url_for, redirect, jsonify
import random
from . import app
from . import webapp
from swanson_app.helpers import getQuoteRating, getUserRating

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/quote")
def get_quote():
    
    # retrieve quote of random id
    id = random.randint(1, 58)
    line = webapp.db.execute("select * from quotes where id = :id", \
        {"id": id}).fetchall()

    # factor out quote information
    quote_id = line[0][0]
    quote = line[0][1]
    word_count = line[0][2]

    # get and format quote rating
    avg_rating = getQuoteRating(quote_id)

    # get user IP
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

    # get users rating
    user_rating = getUserRating(quote_id, str(ip))
    
    # return JSON response with ACAO header
    response = jsonify({
        "id": quote_id,
        "quote": quote,
        "word_count": word_count,
        "author": "Ron Swanson",
        "average_rating": avg_rating,
        "user_rating": user_rating
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

    # factor out quote information
    quote_id = line[0]
    quote = line[1]
    word_count = line[2]

    # get and format rating
    avg_rating = getQuoteRating(quote_id)

    # get user IP
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

    # get users rating
    user_rating = getUserRating(quote_id, str(ip))

    # return json response with ACAO header
    response = jsonify({
        "id": quote_id,
        "quote": quote,
        "word_count": word_count,
        "author": "Ron Swanson",
        "average_rating": avg_rating,
        "user_rating": user_rating
    })
    
    response.headers.add("Access-Control-Allow-Origin", "*")
    
    return response

@app.route("/api/rating", methods = ["POST"])
def rating():
    if request.method == "POST":
        
        # receive post request
        rating = request.get_json()["user_rating"]
        quote_id = request.get_json()["quote_id"]
        user_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        
        # Save rating if not yet rated
        try:
            webapp.db.execute("insert into quote_ratings(quote_id, rating, user_ip) values (:quote_id, :rating, :user_ip)", \
                {"quote_id": quote_id, "rating": rating, "user_ip": user_ip})
            webapp.db.commit()
        except:
            print("no worries, you already rated")
            return "Already rated this one"

        return "Nice work, rating went through!"