# import flask
from flask import Flask, render_template,send_from_directory,request, jsonify, make_response
from flask_cors import CORS, cross_origin

# create the application object
app = Flask(__name__ ,static_folder='build',static_url_path='')
cors = CORS(app)

# config

# use decorators to link the function to a url
@app.route('/test')
def home():
    return {'message': 'Hello, World! bert smells aaa'}


@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')