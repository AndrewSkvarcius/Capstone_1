from app import db
from models import Customers, Products, Orders


db.drop_all()
db.create_all()


