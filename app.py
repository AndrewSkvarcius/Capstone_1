import os

from flask import Flask, render_template, request, flash, redirect, session, g, url_for,jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from send_email import send_email_with_attachment
from models import db, connect_db,Products,Orders,User,Order_item
from forms import AddUserForm, LoginForm,Add_Products,Order_Form


CURR_USER_KEY = "curr_user"
CURRENT_ITEM_KEY = "curr_item"
CURRENT_CART_KEY = "curr_cart"

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

def get_cart_from_session(user_id):
    """Retrieve the user's cart from the session and convert it to a more usable format.

    The cart in the session is a dictionary where the keys are user_ids (as strings) and the values are dictionaries with product_ids as keys and values containing 'quantity' and 'price'.
    This function retrieves the products from the database and returns a dictionary where the keys are product_ids (as integers) and the values are dictionaries with 'product', 'quantity', and 'price'.
    """
    session_cart = session.get('cart', {}).get(str(user_id), {})
    print("Session Cart for User {}: {}".format(user_id, session_cart))

    # Create a new cart with the product objects instead of just the ids
    cart = {}
    for product_id_str, cart_data in session_cart.items():
        if not product_id_str.isdigit() or not isinstance(cart_data, dict):
            continue

        product_id = int(product_id_str)
        product = Products.query.get(product_id)
        if product:
            cart[product_id] = {
                'product': product,
                'quantity': cart_data['quantity'],
                'price': cart_data['price']
            }
    print("Cart for User {}: {}".format(user_id, cart))
    return cart
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

        return redirect("/customers/store")

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

            if user.is_admin:
                return redirect('/admin/orders')
  
        return redirect("/customers/store")

    

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

@app.route('/search_products', methods=['GET', 'POST'])
def search_products():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        print(search_query)
        products = Products.query.filter(Products.product_name.ilike(f'%{search_query}%')).all()
        return render_template("customers/search_results.html", products=products, search_query=search_query)
    
    return render_template("customers/search_results.html")


### Product Routes ###

@app.route("/products/<int:product_id>", methods=["GET"])
def show_product(product_id):
    form = Order_Form(product_id=product_id)
    product = Products.query.get_or_404(product_id)

    return render_template("products/product_show.html", product=product, form=form)


@app.route("/cart")
def cart():
    cart = get_cart_from_session(g.user.id)
    total_price = sum(item['quantity'] * item['price'] for item in cart.values())
    
    total_price = round(total_price, 2)
    return render_template("customers/cart.html", cart=cart, total_price=total_price)


@app.route("/products/add/<int:product_id>", methods=["GET", "POST"])
def add_to_cart(product_id):
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    product_id_str = str(product_id)
    
    quantity= int(request.form.get('quantity'))
    print(product_id)
    
    product = Products.query.get_or_404(product_id)
    if not product or product.quantity < quantity:
        return {"error": "Product not found"}, 400

    user_id = g.user.id
    user_cart = session.get('cart', {}).get(str(user_id), {})

    if product_id_str in user_cart:
        user_cart[product_id_str]['quantity'] += quantity
    else:
        user_cart[product_id_str] = {'quantity': quantity, 'price': float(product.price)}

    cart_data = session.get('cart', {})
    cart_data[str(user_id)] = user_cart
    session['cart'] = cart_data

    print(session['cart'])
    print("!!!!!!Updated Cart:", session['cart'])
    flash( "Item Added", 'success')
    return redirect(url_for("store_render"))  

@app.route('/delete_from_cart/<int:product_id>', methods=["POST", "DELETE"])
def delete_from_cart(product_id):
    if request.method in ['POST', 'DELETE']:
        user_id = g.user.id
        session_cart = session.get('cart', {}).get(str(user_id), {})

        if str(product_id) in session_cart:
            del session_cart[str(product_id)]
            print("********Product with ID {} deleted from cart.".format(product_id))
            print("********Updated Session Cart:", session_cart)
            session.modified = True
            session['cart'][str(user_id)] = session_cart

    return redirect(url_for('cart'))
## Routes where is_admin is true

@app.route('/admin/add_product' , methods=["GET", "POST"])
def add_products():
    form = Add_Products()
    if form.validate_on_submit():
            product = Products(
                product_name=form.product_name.data,
                description=form.description.data,
                image_url=form.image_url.data,
                quantity=form.quantity.data,
                price=form.price.data
                )
            db.session.add(product)    
            db.session.commit()
    return render_template("admin/add_products.html", form=form)

@app.route('/admin/products/<int:product_id>/delete', methods= ["POST", "GET"])
def delete_product(product_id):
    
    if not g.user or not g.user.is_admin:
        flash("Access denied!", "danger")
        return redirect(url_for("login"))
    product = Products.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()


    flash(f"Product {product_id} has been deleted successfully!", "success")

    return redirect(url_for("store_render")) 


@app.route('/admin/orders', methods=["GET", "POST"])
def show_all_orders():
    orders = Orders.query.order_by(Orders.created_at.desc()).all()
    return render_template("admin/admin_orders.html", orders=orders)

@app.route('/admin/order_details/<int:order_id>')

def order_details(order_id):
    
    curr_order = Orders.query.filter_by(id=order_id).first()

    products = Products.query.all()
    product_names = {product.id: product.product_name for product in products}

    return render_template("admin/order_details.html", curr_order=curr_order,products=products,product_names=product_names)

@app.route('/admin/order/<int:order_id>/send_email', methods=['POST'])
def send_email(order_id):

        curr_order = Orders.query.filter_by(id=order_id).first()    

        user = curr_order.user
    
        if request.method == 'POST':
            response = send_email_with_attachment(curr_order,user)
            print(curr_order)
            print (user.email)
            flash("order Submitted successfully")
    
            print("Email sent! Status code: " + str(response.status_code))

        return redirect(url_for("show_all_orders"))



## orders

@app.route('/place_order', methods=['POST'])
def place_order():
    user_id = g.user.id
    session_cart = session.get('cart', {}).get(str(user_id), {})
    
    total_price = 0.0
    order_items = []

    for product_id_str, cart_data in session_cart.items():
        product_id = int(product_id_str)
        product = Products.query.get(product_id)
        if product:
            price = cart_data['price']
            quantity = cart_data['quantity']
            total_price += price * quantity

            order_item = Order_item(product_id=product_id, quantity_sold=quantity, price=price)
            order_items.append(order_item)

    if order_items:
        order = Orders(user_id=user_id, total_price=total_price)
        db.session.add(order)
        db.session.commit()

        for order_item in order_items:
            order_item.order_id = order.id
            db.session.add(order_item)
        db.session.commit()

        session.pop('cart', None)  # Clear the session cart after placing the order

        # Redirect to the order details page for the newly created order
        return redirect(url_for('show_order', order_id=order.id))
    else:
        return jsonify({"error": "No items in the cart to place an order."}), 400



@app.route('/order/<int:order_id>')

def show_order(order_id):
  
    order = Orders.query.filter_by(id=order_id, user_id=g.user.id).first()

    if not order:
        flash("Order not found or unauthorized.", "danger")
        return redirect("/")
    
    products = Products.query.all()
    product_names = {product.id: product.product_name for product in products}
    
    return render_template("customers/show_order.html", order=order, products=products, product_names=product_names)
    
