#!/usr/bin/env python3


# Imports
##############################################################################
from flask import Flask, jsonify, request
import jwt
from datetime import datetime, timedelta
##############################################################################


# Global Values
##############################################################################
app   = Flask(__name__)
PORT  = 5000
DEBUG = True


EXP_T = 1   # Expire Time(Minutes)
##############################################################################


# Configs
##############################################################################
app.config['SECRET_KEY'] = 'Th1s1sTh3Sup3rS3cr3tK3y'
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
            auth_token = jwt.encode(
                {
                 'username':username,
                 'expire':str(datetime.utcnow()+timedelta(minutes=EXP_T))
                },
                app.secret_key
            )

            # If Credentials are Valid
            return jsonify(
                {
                 'message':'Authenticated',
                 'auth_token':auth_token,
                 'status':200
                }
            ),200

    # If Credentials are Invalid
    return jsonify(
        {
         'message':'Credentials are invalid',
         'status':401
         }
    ),401
##############################################################################


# Main
##############################################################################
if __name__ == '__main__':
    app.run(port=PORT,debug=DEBUG)
##############################################################################