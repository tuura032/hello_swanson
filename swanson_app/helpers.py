from . import webapp

def getQuoteRating(quote_id):
    try:
        avg_rating = webapp.db.execute("select avg(rating) from quote_ratings where quote_id = :id", \
                {"id": quote_id}).fetchone()
        avg_rating = avg_rating[0]
        print("LOOK HERE -> first try on avg rating: ", end='')
        print(avg_rating)

        try:
            #avg_rating = int(avg_rating)
            avg_rating = "{:2.1f}".format(avg_rating)
            print(avg_rating)
        except:
            avg_rating = "Can't convert avg rating"
            print(avg_rating)
    
    except:
        print("orignal getQuoteRating didn't work")
        avg_rating = "Not yet rated"

    return avg_rating

def getUserRating(quote_id, ip):
    try:
        user_rating = webapp.db.execute("select rating from quote_ratings where quote_id = :id and user_ip LIKE :ip", \
            {"id": quote_id, "ip": '%'+ip+'%'}).fetchone()
        user_rating = user_rating[0]
    except:
        user_rating = "Not yet rated"
    
    print(user_rating)
    return user_rating