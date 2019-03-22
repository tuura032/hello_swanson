# Entry point for the application.
from . import app    # For application discovery by the 'flask' command. 
from . import views  # For import side-effects of setting up routes. 

from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine('postgres://qthodnlzusljrm:cc6e8a1e7e11920cb59542a4a85ece93c0df62afa20e7fc8ae11af6db0a0443a@ec2-23-23-241-119.compute-1.amazonaws.com:5432/depb4gum4t8d8k')
db = scoped_session(sessionmaker(bind=engine))
