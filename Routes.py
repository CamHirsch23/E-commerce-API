from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/ecommerce_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))

class CustomerAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.Date)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    status = db.Column(db.String(50), default='Pending')
    products = db.relationship('Product', secondary='order_product', backref=db.backref('orders', lazy='dynamic'))

order_product = db.Table('order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
)

# Customer Routes
@app.route('/customer', methods=['POST'])
def create_customer():
    data = request.get_json()
    new_customer = Customer(name=data['name'], email=data['email'], phone=data['phone'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": "Customer created successfully"}), 201

@app.route('/customer/<int:id>', methods=['GET'])
def read_customer(id):
    customer = Customer.query.get(id)
    if customer:
        return jsonify({"id": customer.id, "name": customer.name, "email": customer.email, "phone": customer.phone}), 200
    return jsonify({"message": "Customer not found"}), 404

@app.route('/customer/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    customer = Customer.query.get(id)
    if customer:
        customer.name = data['name']
        customer.email = data['email']
        customer.phone = data['phone']
        db.session.commit()
        return jsonify({"message": "Customer updated successfully"}), 200
    return jsonify({"message": "Customer not found"}), 404

@app.route('/customer/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get(id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"message": "Customer deleted successfully"}), 200
    return jsonify({"message": "Customer not found"}), 404

# CustomerAccount Routes
@app.route('/customer_account', methods=['POST'])
def create_customer_account():
    data = request.get_json()
    new_account = CustomerAccount(username=data['username'], password=data['password'], customer_id=data['customer_id'])
    db.session.add(new_account)
    db.session.commit()
    return jsonify({"message": "Customer account created successfully"}), 201

@app.route('/customer_account/<int:id>', methods=['GET'])
def read_customer_account(id):
    account = CustomerAccount.query.get(id)
    if account:
        customer = Customer.query.get(account.customer_id)
        return jsonify({"id": account.id, "username": account.username, "customer": {"id": customer.id, "name": customer.name}}), 200
    return jsonify({"message": "Customer account not found"}), 404

@app.route('/customer_account/<int:id>', methods=['PUT'])
def update_customer_account(id):
    data = request.get_json()
    account = CustomerAccount.query.get(id)
    if account:
        account.username = data['username']
        account.password = data['password']
        db.session.commit()
        return jsonify({"message": "Customer account updated successfully"}), 200
    return jsonify({"message": "Customer account not found"}), 404

@app.route('/customer_account/<int:id>', methods=['DELETE'])
def delete_customer_account(id):
    account = CustomerAccount.query.get(id)
    if account:
        db.session.delete(account)
        db.session.commit()
        return jsonify({"message": "Customer account deleted successfully"}), 200
    return jsonify({"message": "Customer account not found"}), 404

# Product Routes
@app.route('/product', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product created successfully"}), 201

@app.route('/product/<int:id>', methods=['GET'])
def read_product(id):
    product = Product.query.get(id)
    if product:
        return jsonify({"id": product.id, "name": product.name, "price": product.price}), 200
    return jsonify({"message": "Product not found"}), 404

@app.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = Product.query.get(id)
    if product:
        product.name = data['name']
        product.price = data['price']
        db.session.commit()
        return jsonify({"message": "Product updated successfully"}), 200
    return jsonify({"message": "Product not found"}), 404

@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    return jsonify({"message": "Product not found"}), 404

@app.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    product_list = [{"id": product.id, "name": product.name, "price": product.price} for product in products]
    return jsonify(product_list), 200

# Order Routes
@app.route('/order', methods=['POST'])
def place_order():
    data = request.get_json()
    new_order = Order(order_date=data['order_date'], customer_id=data['customer_id'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order placed successfully"}), 201

@app.route('/order/<int:id>', methods=['GET'])
def retrieve_order(id):
    order = Order.query.get(id)
    if order:
        customer = Customer.query.get(order.customer_id)
        products = [{"id": prod.id, "name": prod.name, "price": prod.price} for prod in order.products]
        return jsonify({"order_id": order.id, "order_date": order.order_date, "customer": {"id": customer.id, "name": customer.name}, "products": products}), 200
    return jsonify({"message": "Order not found"}), 404

@app.route('/order/<int:id>/status', methods=['GET'])
def track_order(id):
    order = Order.query.get(id)
    if order:
        return jsonify({"order_id": order.id, "status": order.status}), 200
    return jsonify({"message": "Order not found"}), 404

@app.route('/customer/<int:customer_id>/orders', methods=['GET'])
def order_history(customer_id):
    orders = Order.query.filter_by(customer_id=customer_id).all()
    order_list = [{"id": order.id, "order_date": order.order_date, "status": order.status} for order in orders]
    return jsonify(order_list), 200

@app.route('/order/<int:id>/cancel', methods=['PUT'])
def cancel_order(id):
    order = Order.query.get(id)
    if order and order.status != 'Shipped':
        order.status = 'Canceled'
        db.session.commit()
        return jsonify({"message": "Order canceled successfully"}), 200
    return jsonify({"message": "Order cannot be canceled"}), 400

@app.route('/order/<int:id>/total', methods=['GET'])
def calculate_order_total(id):
    order = Order.query.get(id)
    if order:
        total_price = sum(product.price for product in order.products)
        return jsonify({"order_id": order.id, "total_price": total_price}), 200
    return jsonify({"message": "Order not found"}), 404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
