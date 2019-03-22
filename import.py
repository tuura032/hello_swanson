import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# engine maintains connection to db
# set DB_URL in terminal
engine = create_engine(os.getenv("URI HERE"))
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
