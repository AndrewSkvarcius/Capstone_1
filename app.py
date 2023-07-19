import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db,Products,Customers,Orders
from forms import AddCustomerForm, LoginForm


CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = (
   os.environ.get('DATABASE_URL', 'postgresql:///your_store'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("customers/home.html")



###### Sign UP/Log in and Log out Customers #####

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = Customers.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = AddCustomerForm()

    if form.validate_on_submit():
        try:
            user = Customers.signup(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=form.password.data,
             )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('customers/signup.html', form=form)

        do_login(user)

        return render_template("customers/store.html")

    else:
        return render_template('customers/signup.html', form=form)

@app.route('/customers/store' )
def store_page():

    return render_template("customers/store.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = Customers.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.email}!", "success")
            return redirect("/customers/store")

        flash("Invalid credentials.", 'danger')

    return render_template('customers/login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""

    # IMPLEMENT THIS
    do_logout()

    flash("You are now logged out" , 'success')
    return redirect('/login')   

### Customer Routes ###

### Product Routes ###

### Admin Routes ###