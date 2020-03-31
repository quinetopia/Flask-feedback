from flask import Flask, jsonify, request, render_template, redirect
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRECT_KEY'] = 'AGRTjgnb;iorbvn;aevnoear'

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

        new_user = User(**data)

        



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
