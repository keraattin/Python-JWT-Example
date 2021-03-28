#!/usr/bin/env python3


# Imports
##############################################################################
from flask import Flask, jsonify, request
import jwt
from datetime import datetime, timedelta
from functools import wraps
import hashlib
##############################################################################


# Global Values
##############################################################################
app   = Flask(__name__)
PORT  = 5000
DEBUG = True


EXP_TIME   = 1              # Expire Time(Minutes)
JWT_ALG    = 'HS256'        # JWT Algorithm
##############################################################################


# Configs
##############################################################################
app.config['SECRET_KEY'] = 'Th1s1sTh3Sup3rS3cr3tK3y'
##############################################################################


# Users {'username':'password'}
##############################################################################
users = {
    'admin':'03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'
} # {'admin':'1234'}
##############################################################################


# Decorators
##############################################################################
def auth_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify(
                {
                    'message':'Token is missing'
                }
            ),403

        try:
            token = jwt.decode(
                auth_header,
                app.secret_key, 
                algorithms=[JWT_ALG]
            )
        except Exception as e:
            return jsonify(
                {
                    'message':'Token is invalid'
                }
            ),403
        
        return f(*args, **kwargs)
    return decorated
##############################################################################


# Views
##############################################################################
# Everyone Can See This
@app.route('/public', methods=['GET'])
def public():
    return 'This is the public page'


# Only Authenticated People See This
@app.route('/private', methods=['GET'])
@auth_token_required
def private():
    return 'This is the private page'


# Login
@app.route('/login', methods=['POST'])
def login():
    credentials = request.get_json()    # Getting Credentials

    # Credentials
    username = credentials['username']
    password = credentials['password']

    # Password Hash
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    # Checking Whether Username & Password Exist or Not
    for usr,passwd in users.items():
        if usr == username and passwd == password_hash:
            auth_token = jwt.encode(
                {
                 'username':username,
                 'exp':datetime.utcnow()+timedelta(minutes=EXP_TIME)
                },
                app.secret_key,     # Secret Key
                JWT_ALG             # JWT Algorithm
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