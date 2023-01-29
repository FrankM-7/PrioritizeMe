from flask import Flask, send_from_directory, request
from firebase_admin import credentials, auth, firestore
import firebase_admin
import json
import pyrebase
import os

app = Flask(__name__, static_folder='build')

cred = credentials.Certificate('google-credentials.json')
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('google-config.json')))
db = firestore.client()

# Sign Up
@app.route('/api/signup', methods=['POST'])
def signup():
    # get the email and password from the request
    email = request.get_json()['email']
    password = request.get_json()['password']
    if email is None or password is None:
        return {'message': 'Error missing email or password'},400
    try:
        # Retrieve the user document with the specified email
        user_ref = db.collection('users').where('email', '==', email).get()

        # print user_ref
        # print (user_ref[0].to_dict())
        
        # If the user exists, return an error
        if len(user_ref) > 0:
            return {'message': 'User already exists'},400

        # Create a new user
        user = auth.create_user(
            email=email,
            password=password
        )

        # Add the user to the database
        db.collection('users').document(user.uid).set({
            'email': email
        })
        
        return {'message': f'Successfully created user {user.uid}'},200
    except:
        return {'message': 'Error creating user'},400

# Login
@app.route('/api/token', methods=['POST'])
def token():
    email = request.get_json()['email']
    password = request.get_json()['password']
    try:
        user = pb.auth().sign_in_with_email_and_password(email, password)
        jwt = user['idToken']
        return {'token': jwt}, 200
    except:
        return {'message': 'There was an error logging in'},400
    
# Get User
@app.route('/api/user', methods=['GET'])
def user():
    token = request.headers.get('Authorization')
    try:
        decoded_token = auth.verify_id_token(token)
        print(decoded_token)
        uid = decoded_token['uid']
        user_ref = db.collection('users').document(uid).get()
        return {'user': user_ref.to_dict()}, 200
    except:
        return {'message': 'There was an error getting the user'},400

# @app.route('/')
# def serve():
#     return send_from_directory(app.static_folder, 'index.html')

#     from flask import Flask, send_from_directory
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')


