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

def getUserUID(token):
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        return uid
    except:
        return None
    
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
            'email': email,
        })
        
        return {'message': f'Successfully created user {user.uid}',
                'status': "success" },200
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
        uid = decoded_token['uid']
        user_ref = db.collection('users').document(uid).get()
        return {'user': user_ref.to_dict()}, 200
    except:
        return {'message': 'There was an error getting the user'},400

# validate token
@app.route('/api/validate', methods=['GET'])
def check_token_validity():
    try:
        decoded_token = auth.verify_id_token(request.headers.get('Authorization'))
        return {'message': 'Token is valid', 'status': 'success'}
    except:
        return {'message': 'Token is invalid', 'status': 'error'}

# add menu to database
@app.route('/api/menu', methods=['POST'])
def add_menu():
    try:
        uid = getUserUID(request.headers.get('Authorization'))
        menu_id = db.collection("users").document(uid).collection("menus").document().id
        db.collection('users').document(uid).collection('menus').document(menu_id).set({
            # get menu from request
            'menu': request.get_json()['name']
        })
        return {'message': 'Menu added successfully', 'status': 'success'}
    except:
        return {'message': 'Error adding menu', 'status': 'error'}

# add submenus to database
@app.route('/api/submenu', methods=['POST'])
def add_submenu():
    try:
        uid = getUserUID(request.headers.get('Authorization'))
        menu_name = request.get_json()['menu']
        menu_id = db.collection("users").document(uid).collection("menus").where('menu', '==', menu_name).get()[0].id
        submenu_id = db.collection("users").document(uid).collection("menus").document(menu_id).collection("submenus").document().id
        db.collection('users').document(uid).collection('menus').document(menu_id).collection('submenus').document(submenu_id).set({
            # get submenu from request
            'submenu': request.get_json()['name'],
            'data': []
        })
        return {'message': 'Submenu added successfully', 'status': 'success'}
    except:
        return {'message': 'Error adding submenu', 'status': 'error'}

# get menus from database
@app.route('/api/user/menus', methods=['GET'])
def get_menus():
    try:
        uid = getUserUID(request.headers.get('Authorization'))
        menus = []
        for menu in db.collection('users').document(uid).collection('menus').get():
            submenus = []
            for submenu in db.collection('users').document(uid).collection('menus').document(menu.id).collection('submenus').get():
                # print(submenu.to_dict()['submenu'])
                submenus.append(submenu.to_dict()['submenu'])
            menus.append({'name' : menu.to_dict()['menu'], 'submenus' : submenus})
        # print(menus)
        return {'menus': menus, 'status': 'success'}
    except:
        return {'message': 'Error getting menus', 'status': 'error'}

# get submenus data from database
@app.route('/api/menu/submenu/data', methods=['GET'])
def get_submenu_data():
    try:
        # get params 
        print('menuId: ' + request.args.get('menuId'))
        print('submenuId: ' + request.args.get('submenuId'))
        uid = getUserUID(request.headers.get('Authorization'))
        # get menu id from menu name matching firbase
        menu_id = db.collection("users").document(uid).collection("menus").where('menu', '==', request.args.get('menuId')).get()[0].id
        submenu_id = db.collection("users").document(uid).collection("menus").document(menu_id).collection("submenus").where('submenu', '==', request.args.get('submenuId')).get()[0].id
        data = db.collection('users').document(uid).collection('menus').document(menu_id).collection('submenus').document(submenu_id).get().to_dict()['data']
        print(data)
        # make an array with [{name: 'name', completed: true}]
        arr = []
        for task in data:
            arr = arr + [{'text': task, 'completed': False}]
        print(arr)
        return {'tasks': arr, 'status': 'success'}
    except:
        return {'message': 'Error getting submenu data', 'status': 'error'}
    
# add task to submenu
@app.route('/api/menu/submenu/data/add', methods=['POST'])
def add_task():
    try:
        # get params 
        print('menuId: ' + request.get_json()['menuId'])
        print('submenuId: ' + request.get_json()['submenuId'])
        uid = getUserUID(request.headers.get('Authorization'))
        # get menu id from menu name matching firbase
        menu_id = db.collection("users").document(uid).collection("menus").where('menu', '==', request.get_json()['menuId']).get()[0].id
        submenu_id = db.collection("users").document(uid).collection("menus").document(menu_id).collection("submenus").where('submenu', '==', request.get_json()['submenuId']).get()[0].id
        
        # add task to submenu
        db.collection('users').document(uid).collection('menus').document(menu_id).collection('submenus').document(submenu_id).update({
            'data': firestore.ArrayUnion([request.get_json()['text']])
        })

        return {'status': 'success'}
    except:
        return {'message': 'Error adding to submenu data', 'status': 'error'}
    
# delete task from submenu
@app.route('/api/menu/submenu/data/delete', methods=['DELETE'])
def delete_task():
    try:
        # get params 
        print("yo")
        print('menuId: ' + request.get_json()['menuId'])
        print('submenuId: ' + request.get_json()['submenuId'])
        uid = getUserUID(request.headers.get('Authorization'))
        # get menu id from menu name matching firbase
        menu_id = db.collection("users").document(uid).collection("menus").where('menu', '==', request.get_json()['menuId']).get()[0].id
        submenu_id = db.collection("users").document(uid).collection("menus").document(menu_id).collection("submenus").where('submenu', '==', request.get_json()['submenuId']).get()[0].id
        
        db.collection('users').document(uid).collection('menus').document(menu_id).collection('submenus').document(submenu_id).update({
            'data': firestore.ArrayRemove([request.get_json()['text']])
        })



        return {'status': 'success'}
    except:
        return {'message': 'Error deleting from submenu data', 'status': 'error'}

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


