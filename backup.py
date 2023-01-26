from flask import Flask, render_template,send_from_directory,request, jsonify, make_response
from flask_cors import CORS, cross_origin
from firebase_admin import credentials, firestore, initialize_app, auth
import pyrebase
import json

import firebase_admin

cred = credentials.Certificate("google-credentials.json")
firebase_admin.initialize_app(cred)

# create the application object
app = Flask(__name__ ,static_folder='build',static_url_path='')
cors = CORS(app)

# Use a service account
cred = credentials.Certificate('google-credentials.json')
# default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('users')
pb = pyrebase.initialize_app(json.load(open('google-config.json')))


# register user
@app.route('/api/register', methods=['POST'])
def register():

    print("hereeeee")
    data = request.get_json()
    email = data['email']
    password = data['password']
    try:
        user = auth.create_user(
            email=email,
            password=password,
        )
        return jsonify({'message': 'User created successfully'}), 200
    except:
        return jsonify({'message': 'User already exists'}), 400

# check if user is logged in
@app.route('/api/verify-session', methods=['GET'])
def verify_session():
    id_token = request.headers.get('Authorization').split(' ')[1]
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']

    user_doc = db.collection('users').document(uid).get()
    if user_doc.exists:
        return jsonify({'isLoggedIn': True}), 200
    else:
        return jsonify({'isLoggedIn': False}), 401

@app.route('/api/check-login', methods=['GET'])
def check_login():
    return jsonify({'isLoggedIn': True}), 200

@app.route('/api/login', methods=['POST'])
def token():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = pb.auth().sign_in_with_email_and_password(email, password)
        jwt = user['idToken']
        return {'token': jwt}, 200
    except:
        return {'message': 'There was an error logging in'},400

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = auth.sign_in_with_email_and_password(email, password)
    except:
        return jsonify({"error": "e.code", "message": "e.message"}), 400
    # do something with the user object, such as setting a session variable
    return jsonify({"message": "Login successful"})


# use decorators to link the function to a url
@app.route('/test')
def home():
    return {'message': 'Hello, World! bert smell s'}

@app.route('/list', methods=['GET'])
def read():
    # get all users
    users_ref = db.collection('users')
    docs = users_ref.stream()
    print(docs)
    return jsonify([doc.to_dict() for doc in docs])

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
