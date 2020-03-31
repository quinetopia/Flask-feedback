from flask import Flask, jsonify, request, \
    render_template, redirect, session

from flask_bcrypt import Bcrypt
from models import db, connect_db, User
from forms import RegUserForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'AGRTjgnb;iorbvn;aevnoear'

bcrypt = Bcrypt()

connect_db(app)
db.create_all()


@app.route('/')
def home_page_redirect():
    """ Redirect to registration page """

    return redirect("/register")

@app.route('/register', methods=['GET', 'POST'])
def registration():
    """ Displays registration page"""

    form = RegUserForm()
    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        
        print(data)
        #eventually move this to User class
        data['password'] = bcrypt.generate_password_hash(data['password'])

        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()

        session['username'] = new_user.username

        return redirect('/secret')
    
    return render_template('registration.html', form=form)









    #     """Add a pet."""

    # form = AddPetForm()

    # if form.validate_on_submit():
    #     data = {k: v for k, v in form.data.items() if k != "csrf_token"}
    #     new_pet = Pet(**data)
    #     # new_pet = Pet(name=form.name.data, age=form.age.data, ...)
    #     db.session.add(new_pet)
    #     db.session.commit()
    #     flash(f"{new_pet.name} added.")
    #     return redirect(url_for('list_pets'))

    # else:
    #     # re-present form for editing
    #     return render_template("pet_add_form.html", form=form)
