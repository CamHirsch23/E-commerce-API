# app.py
from flask import Flask, request, jsonify
from datetime import datetime
from models import db, Customer, CustomerAccount, Product, Order
from schemas import customer_schema, customer_account_schema, product_schema, products_schema, order_schema
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

# Product CRUD Endpoints
@app.route('/products', methods=['POST'])
def add_product():
    try:
        name = request.json['name']
        price = request.json['price']
        stock = request.json['stock']
        new_product = Product(name=name, price=price, stock=stock)
        db.session.add(new_product)
        db.session.commit()
        return product_schema.jsonify(new_product)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = Product.query.get(product_id)
        return product_schema.jsonify(product)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        product = Product.query.get(product_id)
        product.name = request.json['name']
        product.price = request.json['price']
        product.stock = request.json['stock']
        db.session.commit()
        return product_schema.jsonify(product)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        db.session.delete(product)
        db.session.commit()
        return product_schema.jsonify(product)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/products', methods=['GET'])
def get_products():
    try:
        all_products = Product.query.all()
        result = products_schema.dump(all_products)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Order CRUD Endpoints
@app.route('/orders', methods=['POST'])
def place_order():
    try:
        customer_id = request.json['customer_id']
        order_date = datetime.now()
        total_price = request.json['total_price']
        new_order = Order(customer_id=customer_id, order_date=order_date, total_price=total_price)
        db.session.add(new_order)
        db.session.commit()
        return order_schema.jsonify(new_order)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    try:
        order = Order.query.get(order_id)
        return order_schema.jsonify(order)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
