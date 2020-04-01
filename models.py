"""Models for Feedback app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    "Model for our users table"
    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key = True)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(50), unique = True)
    first_name = db.Column(db.String(30), nullable = False)   
    last_name = db.Column(db.String(30), nullable = False)
    feedback = db.relationship("Feedback",
                                backref="user",
                                cascade="all, delete")    

    @classmethod
    def login(cls, username, pwd):
        """Validate that user exists & password is correct.
        Return user if valid; else return False.
        """
        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False
    
    
    @classmethod
    def validate(cls, session_user, username):
        """Validate that the session user matches some other username.
        Returns the user if so, false otherwise."""

        if session_user in db.session.query(User.username).filter_by(username=username).first():
            return User.query.get(username) 
        else:
            return False


    @classmethod
    def create_and_hash(cls, data):
        "Returns new user object with hashed password"
        data['password'] = bcrypt.generate_password_hash(data['password'])
        data['password'] = data['password'].decode("utf8")

        return User(**data)

class Feedback(db.Model):
    "Model for the feedback table."
    __tablename__ = "feedback"

    id = db.Column(db.Integer, 
                   primary_key=True, 
                   auto_increment=True)
    title = db.Column(db.String(100),
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    username = db.Column(db.String(20),
                         db.ForeignKey("users.username"))