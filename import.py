
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# engine maintains connection to db
# set DB_URL in terminal
engine = create_engine("postgres://qthodnlzusljrm:cc6e8a1e7e11920cb59542a4a85ece93c0df62afa20e7fc8ae11af6db0a0443a@ec2-23-23-241-119.compute-1.amazonaws.com:5432/depb4gum4t8d8k")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("quotes.txt")
    reader = f.readlines()
    for quote in reader:
        quote = quote.rstrip()
        quote_length = len(quote.split(' '))
        db.execute("INSERT INTO quotes (quote, quote_length) \
        VALUES (:quote, :quote_length)",
                    {"quote": quote, "quote_length": quote_length})
    db.commit()

    f.close()

if __name__ == "__main__":
    main()
