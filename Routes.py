from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:your_password@localhost/ecommerce_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Models
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)

class CustomerAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Schemas
class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer

class CustomerAccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CustomerAccount

# Initialize schemas
customer_schema = CustomerSchema()
customer_account_schema = CustomerAccountSchema()

# Create the database tables
with app.app_context():
    db.create_all()

# Customer CRUD Endpoints
@app.route('/customers', methods=['POST'])
def add_customer():
    try:
        name = request.json['name']
        email = request.json['email']
        phone = request.json['phone']
        new_customer = Customer(name=name, email=email, phone=phone)
        db.session.add(new_customer)
        db.session.commit()
        return customer_schema.jsonify(new_customer)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    try:
        customer = Customer.query.get(customer_id)
        return customer_schema.jsonify(customer)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    try:
        customer = Customer.query.get(customer_id)
        customer.name = request.json['name']
        customer.email = request.json['email']
        customer.phone = request.json['phone']
        db.session.commit()
        return customer_schema.jsonify(customer)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    try:
        customer = Customer.query.get(customer_id)
        db.session.delete(customer)
        db.session.commit()
        return customer_schema.jsonify(customer)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# CustomerAccount CRUD Endpoints
@app.route('/customer_accounts', methods=['POST'])
def add_customer_account():
    try:
        customer_id = request.json['customer_id']
        username = request.json['username']
        password = request.json['password']
        new_account = CustomerAccount(customer_id=customer_id, username=username, password=password)
        db.session.add(new_account)
        db.session.commit()
        return customer_account_schema.jsonify(new_account)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/customer_accounts/<int:account_id>', methods=['GET'])
def get_customer_account(account_id):
    try:
        account = CustomerAccount.query.get(account_id)
        return customer_account_schema.jsonify(account)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/customer_accounts/<int:account_id>', methods=['PUT'])
def update_customer_account(account_id):
    try:
        account = CustomerAccount.query.get(account_id)
        account.username = request.json['username']
        account.password = request.json['password']
        db.session.commit()
        return customer_account_schema.jsonify(account)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/customer_accounts/<int:account_id>', methods=['DELETE'])
def delete_customer_account(account_id):
    try:
        account = CustomerAccount.query.get(account_id)
        db.session.delete(account)
        db.session.commit()
        return customer_account_schema.jsonify(account)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
