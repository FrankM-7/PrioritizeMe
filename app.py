# import flask
from flask import Flask, render_template, request, redirect, url_for, flash


# create the application object
app = Flask(__name__)

# config

# use decorators to link the function to a url
@app.route('/test')
def home():
    return {'message': 'Hello, World!'}
