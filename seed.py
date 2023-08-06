from app import db
from models import User, Products, Orders, Order_item, Cart_item, Shopping_session


db.drop_all()
db.create_all()



p1 = Products(product_name = "dad hat", description=" Bicycle Day Custom Embroider Hat", image_url ="https://assets.bigcartel.com/product_images/72e63513-46a7-4789-8f5f-054231cd150f/bicycle-day-cap.jpg?auto=format&fit=max&w=346", price= 100.00, quantity=1)
db. session.add(p1)
db.session.commit()

p2 = Products(product_name = "long-sleeve shirt",description=" 70's Ed Donahue Shirt", image_url ="https://www.foralltoenvy.com/cdn/shop/products/grateful_dead_donohue_1_grande.jpg?v=1571262888", price= 500.00, quantity=3)
db. session.add(p2)
db.session.commit()

p3 = Products(product_name = "furry sneakers",description="Nike SB Sneakers", image_url ="https://cdn.flightclub.com/750/TEMPLATE/193085/1.jpg", price= 4459.99, quantity=5)
db. session.add(p3)
db.session.commit()

p4 = Products(product_name = "espo sneakers",description="Nike Steven Powers Sneakers", image_url ="https://images.stockx.com/images/Nike-Air-Force-2-Low-ESPO.png?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color&updated_at=1618255758", price= 399.99, quantity=4)
db. session.add(p4)
db.session.commit()

p5 = Products(product_name = "floyd t-shirt",description="Division Bell Tour Shirt", image_url ="https://throwbackthreadsshop.com/cdn/shop/products/image_69d589fe-9198-4668-b296-8c125e0b3306_2048x2048.jpg?v=1609465392", price= 699.99, quantity=2)
db. session.add(p5)
db.session.commit()


p5 = Products(product_name = "nirvana t-shirt",description="Smell The Spirit", image_url ="https://www.highsnobiety.com/static-assets/thumbor/R_-J5dDW_g0bHKW-hiThmnaFYdU=/1600x1600/www.highsnobiety.com/static-assets/wp-content/uploads/2022/05/09155006/nirvana-merch-heart-shaped-box.jpg", price= 799.99, quantity=1)
db. session.add(p5)
db.session.commit()


