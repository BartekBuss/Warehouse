from flask import Flask, jsonify, send_from_directory, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os

# Ustalenie ścieżki do pliku bazy danych
db_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'warehouse.db')

# Konfiguracja aplikacji Flask i bazy danych
app = Flask(__name__, static_url_path='', static_folder='.')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file_path}'
db = SQLAlchemy(app)

# Define Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Product(name={self.name}, quantity={self.quantity})"

# Create or Update the database schema
with app.app_context():
    db.create_all()

# Endpoint do testowania połączenia frontendu z backendem
@app.route('/api/test', methods=['GET'])
def test_connection():
    return jsonify({"message": "Połączenie z backendem zostało nawiązane poprawnie! Betoniarzu!"})

# Endpoint for retrieving the list of products
@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [{"id": product.id, "name": product.name, "quantity": product.quantity} for product in products]
    return jsonify(product_list)

# Endpoint for adding a new product
@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    if 'name' in data and 'quantity' in data:
        name = data['name']
        quantity = data['quantity']
        new_product = Product(name=name, quantity=quantity)
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"id": new_product.id, "name": new_product.name, "quantity": new_product.quantity}), 201
    else:
        return jsonify({"error": "Missing required fields"}), 400

# Endpoint for deleting a product
@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    else:
        return jsonify({"error": "Product not found"}), 404

# Endpoint for modifying a product
@app.route('/api/products/<int:id>', methods=['PUT'])
def modify_product(id):
    data = request.json
    if 'quantity' in data:
        new_quantity = data['quantity']
        product = Product.query.get(id)
        if product:
            product.quantity = new_quantity
            db.session.commit()
            return jsonify({"id": product.id, "name": product.name, "quantity": product.quantity}), 200
        else:
            return jsonify({"error": "Product not found"}), 404
    else:
        return jsonify({"error": "Missing required fields"}), 400

# Endpoint for handling the main page
@app.route('/')
def index():
    # Pobranie wszystkich produktów z bazy danych
    products = Product.query.all()
    # Renderowanie pliku HTML z przekazaniem produktów jako argumentu
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)