from flask import Flask, render_template,send_from_directory,request, jsonify, make_response
from flask_cors import CORS, cross_origin
from firebase_admin import credentials, firestore, initialize_app


# create the application object
app = Flask(__name__ ,static_folder='build',static_url_path='')
cors = CORS(app)

# Use a service account
cred = credentials.Certificate('google-credentials.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('users')

# config

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