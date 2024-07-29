from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from models import db, Customer, CustomerAccount, Product, Order, OrderItem
from schemas import customer_schema, customer_account_schema, product_schema, products_schema, order_schema, order_item_schema
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Initialize the SQLAlchemy object
db.init_app(app)

# Resources
class CustomerResource(Resource):
    def post(self):
        new_customer = Customer(
            name=request.json['name'],
            email=request.json['email'],
            phone=request.json['phone']
        )
        db.session.add(new_customer)
        db.session.commit()
        return customer_schema.dump(new_customer), 201

    def get(self, id):
        customer = Customer.query.get(id)
        return customer_schema.dump(customer), 200

    def put(self, id):
        customer = Customer.query.get(id)
        customer.name = request.json['name']
        customer.email = request.json['email']
        customer.phone = request.json['phone']
        db.session.commit()
        return customer_schema.dump(customer), 200

    def delete(self, id):
        customer = Customer.query.get(id)
        db.session.delete(customer)
        db.session.commit()
        return '', 204

# Add the resource to the API
api.add_resource(CustomerResource, '/customer/<int:id>')

# Continue with the other resources...

if __name__ == '__main__':
    app.run(debug=True)
