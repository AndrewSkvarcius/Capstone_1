from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()




class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    
    email = db.Column(db.Text,nullable=False,unique=True,)
    
    username = db.Column(db.String(50), unique=True, nullable=False)
    
    password = db.Column(db.Text,nullable=False,)

    is_admin = db.Column(db.Boolean, default=False)
    
    @classmethod
    def signup(cls,email,username, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            
            email=email,
            username=username,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user
     
    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Products(db.Model):

     __tablename__ = 'products'

     id = db.Column(db.Integer, primary_key=True)

     product_name = db.Column(db.Text)

     description = db.Column(db.String(255))

     image_url = db.Column(db.Text, default = "/static/images/default-product-image.png")

     quantity = db.Column(db.Integer, nullable=False)
 
     price = db.Column(db.Float, nullable=False)


class Orders(db.Model):

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='cascade'))

class Order_item(db.Model):

    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True )
    
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='cascade'))

    product_id =  db.Column(db.Integer, db.ForeignKey('products.id', ondelete='cascade'))
    
    quantity_sold = db.Column(db.Integer)

class Shopping_session(db.Model):
     __tablename__ = 'shopping_session'

     id = db.Column(db.Integer, primary_key=True )

     user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))

     total = db.Column(db.Float, nullable=False)

class Cart_item(db.Model):
    __tablename__ = "cart_item"

    id = db.Column(db.Integer, primary_key=True)

    session_id = db.Column(db.Integer, db.ForeignKey("shopping_session.id", ondelete='cascade'))

    product_id = db.Column(db.Integer, db.ForeignKey("products.id", ondelete='cascade'))

    quantity = db.Column(db.Float, nullable=False)

    def __init__(self, item_id, quantity):
        self.item_id = item_id
        self.quantity = quantity
   
def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
   
