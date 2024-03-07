import os
import json
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from models import db, Client, Contract

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app, origins=["http://localhost:3000"])

db.init_app(app)

@app.route('/')
def check():
    return 'Flask is working'

# Universal function to get tables by name
@app.route('/get_table', methods=['GET'])
def get_table():
    # Get the table name from the request parameters
    table_name = request.args.get('tableName', None)
    table_model_map = {
        'clients': Client,  # Add more mappings as needed
        'contracts': Contract,
    }

    # Check if the table name is provided
    if table_name not in table_model_map:
        return Response("Error: Please provide a 'tableName' parameter.", status=400, content_type='text/plain')
    else:
        table_model = table_model_map[table_name]
        table_records = table_model.query.first()
        if table_records:
                
            records_dict = {column.name: getattr(table_records, column.name) for column in table_model.__table__.columns}
            # Use json.dumps to pretty-print the JSON with indentation
            pretty_json = json.dumps(records_dict, indent=2)
            return Response(pretty_json, content_type='application/json; charset=utf-8')
        
    return Response("ERROR")

# Route to add a new user
@app.route('/add_client', methods=['POST'])
def add_clients():
    data = request.get_json()

    companyName = data.get('companyName')
    email = data.get('email')
    firstName = data.get('ownerFirstName')
    lastName = data.get('ownerLastName')
    phone = data.get('ownerPhone')

    new_client = Client(companyName=companyName, 
                      email=email,
                      ownerFirstName=firstName,
                      ownerLastName=lastName,
                      ownerPhone=phone)
    db.session.add(new_client)
    db.session.commit()

    return jsonify({'message': 'Client added successfully'}), 201

# Route to add a new contract
@app.route('/add_contract', methods=['POST'])
def add_contract():
    data = request.get_json()

    new_contract = Contract(
        clientID = data.get('clientID'),
        # totalPrice = data.get('totalPrice'),
        # contractDate = data.get('contractDate'),
        rentDates = data.get('rentDates'),
        firstName = data.get('firstName'),
        lastName = data.get('lastName'),
        email = data.get('email')
    )
    db.session.add(new_contract)
    db.session.commit()

    return jsonify({'message': 'User added successfully'}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
