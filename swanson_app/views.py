from flask import Flask, render_template, session, request, url_for, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import random
from . import app
from . import webapp
from swanson_app.helpers import getQuoteRating, getUserRating, getResponse

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/quote")
def get_quote():
    
    # retrieve quote of random id
    id = random.randint(1, 58)
    try:
        line = webapp.db.execute("select * from quotes where id = :id", {"id": id}).fetchone()
    except:
        line = (1, "Something went wrong", 3)

    response = getResponse(line)

    return response

@app.route("/api/<quote_size>")
def get_quote_sized(quote_size):

    # randomly get one quote from db filtered by size
    try:
        if quote_size == "large":
            line = webapp.db.execute("select * from quotes where id IN (select id from quotes where quote_length > 12) order by RANDOM() LIMIT 1").fetchone()
        elif quote_size == "medium":
            line = webapp.db.execute("select * from quotes where id IN (select id from quotes where quote_length < 13 and quote_length > 4) order by RANDOM() LIMIT 1").fetchone()
        elif quote_size == "small":
            line = webapp.db.execute("select * from quotes where id IN (select id from quotes where quote_length < 5) order by RANDOM() LIMIT 1").fetchone()

    except:
        print("something went wrong api/quote_size")
        line = (1, "Try Again in a moment", 5)

    response = getResponse(line)
    
    return response

@app.route("/api/rating", methods = ["POST"])
def rating():
    if request.method == "POST":
        
        # receive post request
        has_voted = request.get_json()["has_voted"]
        rating = request.get_json()["user_rating"]
        quote_id = request.get_json()["quote_id"]
        user_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

        # Save rating if not yet rated
        if has_voted:
            return "already voted!"
        webapp.db.execute("insert into quote_ratings(quote_id, rating, user_ip) values (:quote_id, :rating, :user_ip)", \
            {"quote_id": quote_id, "rating": rating, "user_ip": user_ip})
        webapp.db.commit()

        #response = "vote confirmed"
        #response.headers.add("Acess-Control-Allow-Origin", "*")

        return "vote confirmed"