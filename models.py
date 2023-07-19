from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class Products(db.Model):

     __tablename__ = 'products'

     id = db.Column(
        db.Integer, 
        primary_key=True
        )

     product_name = db.Column(
        db.Text
     )

     image_url = db.Column(
        db.Text, 
        default = "/static/images/default-product-image.png"
        )
 
     price = db.Column(
        db.Integer, 
        nullable=False
        )

     quanity = db.Column(
        db.Integer, nullable=False
        )

class Customers(db.Model):

     __tablename__ = 'customers'

     id = db.Column(
        db.Integer, 
        primary_key=True
        )

     first_name = db.Column(
        db.Text
        )

     last_name = db.Column(
        db.Text
        )
 
     email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
     )

     password = db.Column(
        db.Text,
        nullable=False,
    )    
    
     @classmethod
     def signup(cls, first_name, last_name, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = Customers(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user
     
     @classmethod
     def authenticate(cls, email, password):
        """Find user with `email` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(email=email).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Orders(db.Model):

    __tablename__ = "orders"

    order_id = db.Column(
        db.Integer, 
        primary_key=True
        )


    product_id = db.column(
        db.Integer, 
        db.ForeignKey("products.id")
        )

    customer_id = db.Column(
        db.Integer, 
        db.ForeignKey("customers.id")
        )


   









def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)

