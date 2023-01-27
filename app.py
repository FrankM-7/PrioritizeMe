import firebase_admin
import pyrebase
from firebase_admin import credentials, auth
import json
from flask import Flask, request, send_from_directory
from functools import wraps

app = Flask(__name__ ,static_folder='build',static_url_path='')
cred = credentials.Certificate('google-credentials.json')
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('google-config.json')))

def check_token(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if not request.headers.get('authorization'):
            return {'message': 'No token provided'},400
        try:
            user = auth.verify_id_token(request.headers['authorization'])
            request.user = user
        except:
            return {'message':'Invalid token provided.'},400
        return f(*args, **kwargs)
    return wrap

@app.route('/api/userinfo')
@check_token
def userinfo():
    # Verify the token and get the user data
    try:
        token = request.headers['authorization']
        decoded_token = auth.verify_id_token(token)
        user_id = decoded_token['uid']
        user_data = auth.get_user(user_id)
    except auth.AuthError as e:
        print(e)
    return {'data': user_data.email}, 200

@app.route('/api/signup', methods=['POST'])
def signup():
    # get the email and password from the request
    email = request.get_json()['email']
    password = request.get_json()['password']
    print(email)
    print(password)
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

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')