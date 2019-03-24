from . import webapp
from flask import request, jsonify
from sqlalchemy.orm import scoped_session, sessionmaker

def getQuoteRating(quote_id):
    try:
        avg_rating = webapp.db.execute("select avg(rating) from quote_ratings where quote_id = :id", \
                {"id": quote_id}).fetchone()
        avg_rating = avg_rating[0]

        try:
            avg_rating = "{:2.1f}".format(avg_rating)
            print(avg_rating)
        except:
            avg_rating = "Not yet rated"
            print(avg_rating)
    
    except:
        avg_rating = "Not yet rated"

    print(avg_rating, end='')
    print(avg_rating)
    return avg_rating

def getUserRating(quote_id, ip):
    try:
        user_rating = webapp.db.execute("select rating from quote_ratings where quote_id = :id and user_ip LIKE :ip", \
            {"id": quote_id, "ip": '%'+ip+'%'}).fetchone()
        user_rating = user_rating[0]
    except:
        user_rating = "Not yet rated"
    
    print("user_rating: ", end='')
    print(user_rating)
    return user_rating

def getResponse(line):
    # factor out quote information
    quote_id = line[0]
    quote = line[1]
    word_count = line[2]

    # get and format quote rating
    avg_rating = getQuoteRating(quote_id)

    # get user IP
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

    # get users rating
    user_rating = getUserRating(quote_id, str(ip))

    # send boolean if user has voted or not
    if user_rating == "Not yet rated":
        has_voted = False
    else:
        has_voted = True
    
    # return JSON response with ACAO header
    response = jsonify({
        "id": quote_id,
        "quote": quote,
        "word_count": word_count,
        "author": "Ron Swanson",
        "average_rating": avg_rating,
        "user_rating": user_rating,
        "has_voted": has_voted
    })

    response.headers.add("Access-Control-Allow-Origin", "*")

    return response