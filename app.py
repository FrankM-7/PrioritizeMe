from flask import Flask, send_from_directory, request
from firebase_admin import credentials, auth
import firebase_admin
import json
import pyrebase
import os

app = Flask(__name__, static_folder='build')

cred = credentials.Certificate('google-credentials.json')
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('google-config.json')))

@app.route('/api/signup', methods=['POST'])
def signup():
    # get the email and password from the request
    email = request.get_json()['email']
    password = request.get_json()['password']
    if email is None or password is None:
        return {'message': 'Error missing email or password'},400
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return {'message': f'Successfully created user {user.uid}'},200
    except:
        return {'message': 'Error creating user'},400

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


