"""Models for Feedback app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key = True)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(50), unique = True)
    first_name = db.Column(db.String(30), nullable = False)   
    last_name = db.Column(db.String(30), nullable = False)    

