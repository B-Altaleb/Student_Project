# Server File

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

@app.route('/')
def home():
    return "Connected to server successfully"

app.config['MONGO_URI'] = 'mongodb+srv://shivanihe22817:shivani#786@cluster0.mjfivyq.mongodb.net/restfuldatabase?retryWrites=true&w=majority'
mongo = PyMongo(app)

#Add a new patient record
@app.route('/patients', methods=['POST'])
def create_patient():
    headers = {'Content-Type': 'application/json'}
    email = request.json['email']
    existing_patient = mongo.db.patients.find_one({'email': email})
    if existing_patient:
        response = {'message': 'Patient with email {} already exists'.format(email)}
        return jsonify(response), 409, headers
    else:
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        age = request.json['age']
        gender = request.json['gender']
        address = request.json['address']
        symptom_fever = request.json['symptom_fever']
        symptom_cough = request.json['symptom_cough']
        patient_id = mongo.db.patients.insert_one({'first_name': first_name, 'last_name' : last_name,
                                                   'age': age, 'gender': gender, 'address': address,
                                                   'email': email, 'symptom_fever': symptom_fever,
                                                   'symptom_cough': symptom_cough}).inserted_id
        new_patient = mongo.db.patients.find_one({'_id': patient_id})
        response = {
            'id': str(new_patient['_id']),
            'first_name' : new_patient['first_name'],
            'last_name' : new_patient['last_name'],
            'age' : new_patient['age'],
            'gender' : new_patient['gender'],
            'address' : new_patient['address'],
            'email' : new_patient['email'],
            'symptom_fever' : new_patient['symptom_fever'],
            'symptom_cough' : new_patient['symptom_cough']
        }
        return jsonify(response), 200, headers

#Get all patients
@app.route('/patients', methods=['GET'])
def get_all_patients():
    headers = {'Content-Type': 'application/json'}
    patients = mongo.db.patients.find()
    response = []
    for patient in patients:
        response.append({
            'id': str(patient['_id']),
            'first_name' : patient['first_name'],
            'last_name' : patient['last_name'],
            'age' : patient['age'],
            'gender' : patient['gender'],
            'address' : patient['address'],
            'email' : patient['email'],
            'symptom_fever' : patient['symptom_fever'],
            'symptom_cough' : patient['symptom_cough']
        })
    return jsonify(response), 200, headers

#Get a specific patient record
@app.route('/patients/<first_name>/<last_name>', methods=['GET'])
def get_patient(first_name, last_name):
    headers = {'Content-Type': 'application/json'}
    patient = mongo.db.patients.find_one({'first_name': first_name, 'last_name': last_name})
    if patient:
        response = {
            'id': str(patient['_id']),
            'first_name' : patient['first_name'],
            'last_name' : patient['last_name'],
            'age' : patient['age'],
            'gender' : patient['gender'],
            'address' : patient['address'],
            'email' : patient['email'],
            'symptom_fever' : patient['symptom_fever'],
            'symptom_cough' : patient['symptom_cough']
        }
    else:
        response = {'message': 'patient not found'}
    return jsonify(response), 200, headers

#Update a specific patient record
@app.route('/patients/<first_name>/<last_name>', methods=['PUT'])
def update_patient(first_name, last_name):
    headers = {'Content-Type': 'application/json'}
    patient = mongo.db.patients.find_one({'first_name': first_name, 'last_name': last_name, 'email': request.json.get('email')})
    if patient:
        age = request.json.get('age', patient['age'])
        gender = request.json.get('gender', patient['gender'])
        address = request.json.get('address', patient['address'])
        email = request.json.get('email', patient['email'])
        symptom_fever = request.json.get('symptom_fever', patient['symptom_fever'])
        symptom_cough = request.json.get('symptom_cough', patient['symptom_cough'])
        mongo.db.patients.update_one({'_id': patient['_id']},{'$set': {'first_name': first_name, 'last_name' : last_name,
                                           'age': age, 'gender': gender, 'address': address,
                                           'email': email, 'symptom_fever': symptom_fever,
                                           'symptom_cough': symptom_cough}})
        updated_patient = mongo.db.patients.find_one({'first_name': first_name, 'last_name': last_name, 'email': email})
        response = {
            'id': str(updated_patient['_id']),
            'first_name': updated_patient['first_name'],
            'last_name': updated_patient['last_name'],
            'age': updated_patient['age'],
            'gender': updated_patient['gender'],
            'address': updated_patient['address'],
            'email': updated_patient['email'],
            'symptom_fever': updated_patient['symptom_fever'],
            'symptom_cough': updated_patient['symptom_cough']
        }
    else:
        response = {'message': 'patient not found'}
    return jsonify(response), 200, headers



#Delete a patient record
@app.route('/patients/<first_name>/<last_name>', methods=['DELETE'])
def delete_patient(first_name, last_name):
    headers = {'Content-Type': 'application/json'}
    result = mongo.db.patients.delete_one({'first_name': first_name, 'last_name': last_name})
    if result.deleted_count == 1:
        response = {'message': 'patient deleted successfully'}
    else:
        response = {'message': 'patient not found'}
    return jsonify(response), 200, headers


if __name__ == '__main__':
   app.run(debug= True)

