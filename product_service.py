# ASSIGNENT 2: 
# DAVID NEWMAN
# CMSC 455
# product_service.py

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product.db'
db = SQLAlchemy(app)


# PRODUCT: DATA STRUCTURE: 
class Product(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(50))
    price       = db.Column(db.Float)
    quantity    = db.Column(db.Integer)

    # JSON_OUTPUT PROPERTY HANDLER FOR OUTPUTING DATA: 
    @property
    def json_output(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity
        }


# PRODUCTS: FUNCTION: (GET/MAKE PRODUCTS)
@app.route('/products', methods = ['GET', 'POST'])
def products():
    # GET PRODUCT INFO FROM DATABASE: 
    if request.method == 'GET':
        # RETRIEVE ALL PRODUCTS FROM THE DATABASE: 
        products = Product.query.all()

        # GRAB THE PRODUCTS AND RETURN IT'S JSON FILE: 
        return jsonify([product.json_output for product in products])
    
    # MAKE A PRODUCT: 
    elif request.method == 'POST':
        # NEW PRODUCT CREATION: 
        new_product = Product(name = request.json['name'], price = request.json['price'], quantity = request.json['quantity'])

        # ADD AND COMMIT THE PRODUCT TO THE DATABASE: 
        db.session.add(new_product)
        db.session.commit()

        # RETURN THE JSONIFIED PRODUCT INFO AND CONFIRM IT WITH CODE: 201
        return jsonify(new_product.json_output), 201

# GET PRODUCT: FUNCTION: (VIA PRODUCT ID PARAM.)
@app.route('/products/<int:product_id>', methods = ['GET'])
def get_product(product_id):
    return jsonify(Product.query.get_or_404(product_id).json_output)


# CREATE DATABASE TABLES: FUNCTION: 
@app.before_first_request
def create_tables():
    db.create_all()

# RUN THE APP! 
if __name__ == '__main__':
    app.run(debug = True)