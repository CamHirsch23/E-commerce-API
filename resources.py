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

class CustomerAccountResource(Resource):
    def post(self):
        new_account = CustomerAccount(
            username=request.json['username'],
            password=request.json['password'],
            customer_id=request.json['customer_id']
        )
        db.session.add(new_account)
        db.session.commit()
        return customer_account_schema.dump(new_account), 201

    def get(self, id):
        account = CustomerAccount.query.get(id)
        return customer_account_schema.dump(account), 200

    def put(self, id):
        account = CustomerAccount.query.get(id)
        account.username = request.json['username']
        account.password = request.json['password']
        db.session.commit()
        return customer_account_schema.dump(account), 200

    def delete(self, id):
        account = CustomerAccount.query.get(id)
        db.session.delete(account)
        db.session.commit()
        return '', 204

class ProductResource(Resource):
    def post(self):
        new_product = Product(
            name=request.json['name'],
            price=request.json['price']
        )
        db.session.add(new_product)
        db.session.commit()
        return product_schema.dump(new_product), 201

    def get(self, id):
        product = Product.query.get(id)
        return product_schema.dump(product), 200

    def put(self, id):
        product = Product.query.get(id)
        product.name = request.json['name']
        product.price = request.json['price']
        db.session.commit()
        return product_schema.dump(product), 200

    def delete(self, id):
        product = Product.query.get(id)
        db.session.delete(product)
        db.session.commit()
        return '', 204

class ProductListResource(Resource):
    def get(self):
        all_products = Product.query.all()
        return products_schema.dump(all_products), 200

class OrderResource(Resource):
    def post(self):
        new_order = Order(
            customer_id=request.json['customer_id'],
            order_date=datetime.now()
        )
        db.session.add(new_order)
        db.session.commit()
        return order_schema.dump(new_order), 201

    def get(self, id):
        order = Order.query.get(id)
        return order_schema.dump(order), 200
