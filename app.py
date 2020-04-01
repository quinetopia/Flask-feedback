from flask import Flask, jsonify, request, \
    render_template, redirect, session, flash

from flask_bcrypt import Bcrypt
from models import db, connect_db, User, Feedback
from forms import RegUserForm, LoginUserForm, AddFeedbackForm, EditFeedbackForm

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
        
        new_user = User.create_and_hash(data)
        db.session.add(new_user)
        db.session.commit()

        session['username'] = new_user.username

        return redirect(f'/users/{new_user.username}')
    
    return render_template('registration.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Displays login page"""

    form = LoginUserForm()
    
    if form.validate_on_submit():
        
        user = User.login(form.username.data, form.password.data)
        
        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")
        
        else:
            form.username.errors = ["Bad username or password"]

    return render_template('login.html', form=form)


@app.route("/users/<username>")
def profile(username):
    """Displays the info for the <username> user if they are vaidated in the session
    Redirects to home page otherwise."""

    session_user = session.get("username", None)
    
    user = User.validate(session_user, username)
    
    if user:    
        return render_template("profile.html",
                               user=user)
    
    flash("Invalid user")
    return redirect("/")


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Deletes <username> user and redirect to home page if
    validated by the session, simply redirects to home page otherwise."""
    
    target_user = User.query.get_or_404(username)

    session_user = session.get("username", None)
    
    user = User.validate(session_user, username)
    
    if user:
        db.session.delete(target_user)
        db.session.commit()
        flash(f"User {target_user.username} deleted!")
        return redirect("/")

    flash("Invalid user")
    return redirect(f"/register")


@app.route("/logout")
def logout():
    "Removes username from the session"

    if "username" in session:
        del session["username"]

    return redirect("/")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """ On GET: If <username> is in the session, shows add feedback form"""
    
    form = AddFeedbackForm()

    session_user = session.get("username", None)
    
    user = User.validate(session_user, username)
    
    if user:    
        
        if form.validate_on_submit():
            data = {k: v for k, v in form.data.items() if k != "csrf_token"}
            
            data["username"] = username

            new_feedback = Feedback(**data) 

            db.session.add(new_feedback)
            db.session.commit()
        
            return redirect(f"/users/{username}")

        else:
            return render_template("feedback.html",
                                    form=form)

    flash("Invalid user!")
    return redirect(f"/")


@app.route("/feedback/<feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    "Show form for editing feedback."
    
    current_feedback = Feedback.query.get_or_404(feedback_id)

    form = EditFeedbackForm(obj=current_feedback)

    session_user = session.get("username", None)
    
    user = User.validate(session_user, current_feedback.username)
    
    if user:    
        
        if form.validate_on_submit():
            data = {k: v for k, v in form.data.items() if k != "csrf_token"}
            
            current_feedback.title = data["title"]
            current_feedback.content = data["content"]

            db.session.commit()
        
            return redirect(f"/users/{current_feedback.username}")
        else:
            return render_template("editfeedback.html",
                                    form=form)

    flash("Invalid user!")
    return redirect(f"/register")


@app.route("/feedback/<feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    "Delete feedback and redirect user to their profile."
    
    current_feedback = Feedback.query.get_or_404(feedback_id)

    session_user = session.get("username", None)
    user = User.validate(session_user, current_feedback.username)
    
    if user:
        db.session.delete(current_feedback)
        db.session.commit()
        flash(f"Feedback {current_feedback.title} deleted!")
        return redirect(f"/users/{current_feedback.username}")

    flash("Please log in!")
    return redirect(f"/register")


