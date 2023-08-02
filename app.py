import os

from flask import Flask, render_template, request, flash, redirect, session, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db,Products,Orders,User
from forms import AddUserForm, LoginForm, AdminLogin, AddAdminForm,Order_Form


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

### Customer routes ###
###### Sign UP/Log in and Log out Customers #####

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("customers/home.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = AddUserForm()

    if form.validate_on_submit():
        try:
            user = User.signup(

                email=form.email.data,
                username=form.username.data,
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


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
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

@app.route('/customers/store', methods=["GET", "POST"])
def store_render():
   
   form = Order_Form()
   products= Products.query.all()
   
   return render_template("customers/store.html", products=products, form=form)


### Product Routes ###

@app.route("/products/<int:product_id>", methods=["GET"])
def show_product(product_id):
    form = Order_Form(product_id=product_id)
    product = Products.query.get_or_404(product_id)

    return render_template("products/product_show.html", product=product, form=form)


@app.route('/add_to_order', methods=['POST'])
def add_to_order():
   
   form = Order_Form()
   
   if form.validate_on_submit():
    
    product_id = request.form[product_id]
    product = Products.query.get_or_404(product_id)
    if product:
        quantity = form.quanity.data
        order = Orders(product_id=product_id, quantity=quantity)
        db.session.add(order)
        db.session.commit()
        return f"Added {quantity} {product.name}(s) to order successfully"
    else:
       
     return url_for("add_to_order")   

### Admin Routes ###
 
@app.route("/admin/login" , methods=["GET", "POST"])
def admin_login():
     
    form = AdminLogin()

    if form.validate_on_submit():
        user = Admin.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {Admin.username}!", "success")
            return redirect("/admin/orders")

        flash("Invalid credentials.", 'danger')

    return render_template('admin/admin_login.html', form=form)

@app.route("/admin/create" , methods=["GET", "POST"])
def create():
    """Handle Admin signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = AddAdminForm()

    if form.validate_on_submit():
        try:
            user = Admin.create(
                username=form.username.data,
                password=form.password.data,
             )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('admin/admin_signup.html', form=form)

        do_login(user)

        return render_template("admin/admin_login.html")

    else:
        return render_template('admin/admin_signup.html', form=form)

@app.route("/admin/orders" , methods=["GET", "POST"])
def admin_orders():
    
    return render_template("admin/admin_orders.html")