#schemas/__init__.py


from flask_marshmallow import Marshmallow

ma = Marshmallow()

#schemas/customer_schema.py


from . import ma
from models.customer import Customer

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

#schemas/customer_account_schema.py


from . import ma
from models.customer_account import CustomerAccount

class CustomerAccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CustomerAccount
        load_instance = True

customer_account_schema = CustomerAccountSchema()
customer_accounts_schema = CustomerAccountSchema(many=True)

#schemas/product_schema.py


from . import ma
from models.product import Product

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

#schemas/order_schema.py


from . import ma
from models.order import Order

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

#schemas/order_item_schema.py


from . import ma
from models.order_item import OrderItem

class OrderItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItem
        load_instance = True

order_item_schema = OrderItemSchema()
order_items_schema = OrderItemSchema(many=True)
