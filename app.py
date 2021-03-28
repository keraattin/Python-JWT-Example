#!/usr/bin/env python3


# Imports
##############################################################################
from flask import Flask, jsonify, request
##############################################################################


# Global Values
##############################################################################
app   = Flask(__name__)
PORT  = 5000
DEBUG = True
##############################################################################


# Users {'username':'password'}
##############################################################################
users = {
    'admin':'1234'
}
##############################################################################


# Views
##############################################################################
@app.route('/')
def home():
    return 'Home Page'


@app.route('/login', methods=['POST'])
def login():
    credentials = request.get_json()

    username = credentials['username']
    password = credentials['password']

    for usr,passwd in users.items():
        if usr == username and passwd == password:
            return jsonify({'message':'Authenticated',
                            'status':200}),200

    return jsonify({'message':'Credentials are invalid',
                    'status':401}),401
##############################################################################


# Main
##############################################################################
if __name__ == '__main__':
    app.run(port=PORT,debug=DEBUG)
##############################################################################