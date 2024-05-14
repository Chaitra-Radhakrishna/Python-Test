from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///address_book.db'
db = SQLAlchemy(app)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __init__(self, street, city, state, postal_code, latitude, longitude):
        self.street = street
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.latitude = latitude
        self.longitude = longitude

# Endpoint to create an address
@app.route('/addresses', methods=['POST'])
def create_address():
    data = request.get_json()
    new_address = Address(**data)
    db.session.add(new_address)
    db.session.commit()
    return jsonify({'message': 'Address created successfully'}), 201

# Endpoint to update an address
@app.route('/addresses/<int:address_id>', methods=['PUT'])
def update_address(address_id):
    data = request.get_json()
    address = Address.query.get(address_id)
    if not address:
        return jsonify({'message': 'Address not found'}), 404
    for key, value in data.items():
        setattr(address, key, value)
    db.session.commit()
    return jsonify({'message': 'Address updated successfully'}), 200

# Endpoint to delete an address
@app.route('/addresses/<int:address_id>', methods=['DELETE'])
def delete_address(address_id):
    address = Address.query.get(address_id)
    if not address:
        return jsonify({'message': 'Address not found'}), 404
    db.session.delete(address)
    db.session.commit()
    return jsonify({'message': 'Address deleted successfully'}), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
