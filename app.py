from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:LuckyFrytki123!@localhost/warehouse_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float(10, 2), nullable=False)
    type = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Product(name={self.name}, quantity={self.quantity}, price={self.price}, type={self.type})"


with app.app_context():
    db.create_all()


@app.route('/api/test', methods=['GET'])
def test_connection():
    return jsonify({"message": "Połączenie z backendem zostało nawiązane poprawnie!"})


@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [{"id": product.id, "name": product.name, "quantity": product.quantity, "price": round(product.price, 2), "type": product.type} for product in products]
    return jsonify(product_list)


@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    if 'name' in data and 'quantity' in data and 'price' in data and 'type' in data:
        name = data['name']
        quantity = data['quantity']
        price = data['price']
        type = data['type']
        new_product = Product(name=name, quantity=quantity, price=price, type=type)
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"id": new_product.id, "name": new_product.name, "quantity": new_product.quantity, "price": new_product.price, "type": new_product.type}), 201
    else:
        return jsonify({"error": "Missing required fields"}), 400


@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    else:
        return jsonify({"error": "Product not found"}), 404


@app.route('/api/products/<int:id>', methods=['PUT'])
def modify_product(id):
    data = request.json
    if 'quantity' in data and 'price' in data and 'type' in data:
        new_quantity = data['quantity']
        new_price = data['price']
        new_type = data['type']
        product = Product.query.get(id)
        if product:
            product.quantity = new_quantity
            product.price = new_price
            product.type = new_type
            db.session.commit()
            return jsonify({"id": product.id, "name": product.name, "quantity": product.quantity, "price": product.price, "type": product.type}), 200
        else:
            return jsonify({"error": "Product not found"}), 404
    else:
        return jsonify({"error": "Missing required fields"}), 400


@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


if __name__ == '__main__':
    app.run(debug=True)



#pyjwt
#user sie loguje (formatka do logowania i rejestracji), po logowaniu backend zwraca token któy za pisujesz w cookies albo localstorage 
#za każdym razem jak chcesz coś zmienić w bazie, sprawdzic czy request jest autoryzowany
#2 opcje: 
#- zrobić w html modal  i JS wyświetlić że błędnme dane
#-import bootstrap i wyświetlenie modala 