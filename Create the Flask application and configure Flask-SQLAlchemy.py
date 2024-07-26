import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Initialize Flask app
app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+mysqlconnector://root:your_password@localhost/ecommerce_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Customer(db.Model):
    """Model for the customers table"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)


class CustomerAccount(db.Model):
    """Model for the customer accounts table"""
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Product(db.Model):
    """Model for the products table"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)


class Order(db.Model):
    """Model for the orders table"""
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.Float, nullable=False)


class OrderItem(db.Model):
    """Model for the order items table"""
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    """Schema for the Customer model"""
    class Meta:
        model = Customer


class CustomerAccountSchema(ma.SQLAlchemyAutoSchema):
    """Schema for the CustomerAccount model"""
    class Meta:
        model = CustomerAccount


class ProductSchema(ma.SQLAlchemyAutoSchema):
    """Schema for the Product model"""
    class Meta:
        model = Product


class OrderSchema(ma.SQLAlchemyAutoSchema):
    """Schema for the Order model"""
    class Meta:
        model = Order


class OrderItemSchema(ma.SQLAlchemyAutoSchema):
    """Schema for the OrderItem model"""
    class Meta:
        model = OrderItem


# Initialize schemas
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
customer_account_schema = CustomerAccountSchema()
customer_accounts_schema = CustomerAccountSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
order_item_schema = OrderItemSchema()
order_items_schema = OrderItemSchema(many=True)

# Create the database tables
with app.app_context():
    db.create_all()


@app.route('/customers', methods=['POST'])
def add_customer():
    """Add a new customer"""
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']
    new_customer = Customer(name=name, email=email, phone=phone)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer)


@app.route('/customers', methods=['GET'])
def get_customers():
    """Retrieve all customers"""
    all_customers = Customer.query.all()
    result = customers_schema.dump(all_customers)
    return jsonify(result)


@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Retrieve a customer by ID"""
    customer = Customer.query.get(customer_id)
    return customer_schema.jsonify(customer)


@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """Update a customer by ID"""
    customer = Customer.query.get(customer_id)
    customer.name = request.json['name']
    customer.email = request.json['email']
    customer.phone = request.json['phone']
    db.session.commit()
    return customer_schema.jsonify(customer)


@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """Delete a customer by ID"""
    customer = Customer.query.get(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return customer_schema.jsonify(customer)


@app.route('/customer_accounts', methods=['POST'])
def add_customer_account():
    """Add a new customer account"""
    customer_id = request.json['customer_id']
    username = request.json['username']
    password = request.json['password']
    new_account = CustomerAccount(customer_id=customer_id, username=username, password=password)
    db.session.add(new_account)
    db.session.commit()
    return customer_account_schema.jsonify(new_account)


@app.route('/customer_accounts', methods=['GET'])
def get_customer_accounts():
    """Retrieve all customer accounts"""
    all_accounts = CustomerAccount.query.all()
    result = customer_accounts_schema.dump(all_accounts)
    return jsonify(result)


@app.route('/customer_accounts/<int:account_id>', methods=['GET'])
def get_customer_account(account_id):
    """Retrieve a customer account by ID"""
    account = CustomerAccount.query.get(account_id)
    return customer_account_schema.jsonify(account)


@app.route('/customer_accounts/<int:account_id>', methods=['PUT'])
def update_customer_account(account_id):
    """Update a customer account by ID"""
    account = CustomerAccount.query.get(account_id)
    account.username = request.json['username']
    account.password = request.json['password']
    db.session.commit()
    return customer_account_schema.jsonify(account)


@app.route('/customer_accounts/<int:account_id>', methods=['DELETE'])
def delete_customer_account(account_id):
    """Delete a customer account by ID"""
    account = CustomerAccount.query.get(account_id)
    db.session.delete(account)
    db.session.commit()
    return customer_account_schema.jsonify(account)


@app.route('/products', methods=['POST'])
def add_product():
    """Add a new product"""
    name = request.json['name']
    price = request.json['price']
    stock = request.json['stock']
    new_product = Product(name=name, price=price, stock=stock)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)


@app.route('/products', methods=['GET'])
def get_products():
    """Retrieve all products"""
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Retrieve a product by ID"""
    product = Product.query.get(product_id)
    return product_schema.jsonify(product)


@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update a product by ID"""
    product = Product.query.get(product_id)
    product.name = request.json['name']
    product.price = request.json['price']
    product.stock = request.json['stock']
    db.session.commit()
    return product_schema.jsonify(product)


@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product by ID"""
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)


@app.route('/orders', methods=['POST'])
def place_order():
    """Place a new order"""
    customer_id = request.json['customer_id']
    order_date = datetime.now()
    total_price = 0
    new_order = Order(customer_id=customer_id, order_date=order_date, total_price=total_price)
    db.session.add(new_order)
    db.session.commit()

    order_items = request.json['order_items']
    for item in order_items:
        product_id = item['product_id']
        quantity = item['quantity']
        price = item['price']
        total_price += price * quantity
        new_order_item = OrderItem(
            order_id=new_order.id, product_id=product_id, quantity=quantity, price=price)
        db.session.add(new_order_item)

    new_order.total_price = total_price
    db.session.commit()
    return order_schema.jsonify(new_order)


@app.route('/orders', methods=['GET'])
def get_orders():
    """Retrieve all orders"""
    all_orders = Order.query.all()
    result = orders_schema.dump
