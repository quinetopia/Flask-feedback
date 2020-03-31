from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError
from wtforms.validators import Length, InputRequired, Email

from models import User

class RegUserForm(FlaskForm):
    """ User registration form"""

    def validate_username(form, field):
        """ Validate username is unique """
        if User.query.filter(User.username==field.data).first():
            raise ValidationError("User name already in use.")

    username = StringField("Username: ", 
                validators=[validate_username, Length(max=20), InputRequired()])
    password = PasswordField("Password: ", 
                validators=[InputRequired()])
    email = StringField("Email: ",
                validators=[Email(message="Please enter a valid email"), 
                            InputRequired(), Length (max=50)])
    first_name = StringField("First name: ",
                validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last name: ",
                validators=[InputRequired(), Length(max=30)])





