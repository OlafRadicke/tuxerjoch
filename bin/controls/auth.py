# -*- coding: utf-8 -*-

import bottle
import json
import datetime
import uuid
import hashlib
import logging

class Auth:

    def __init__(self, couchDB):
        self.couchDB = couchDB


    def hash_password( self, password ):
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
        # print( hashlib.sha256("tuxerjoch".encode() + tuxerjoch.encode()).hexdigest() + ':' + "tuxerjoch" )

    def check_password( self, input_password ):
        response = self.couchDB.getDocValue( "auth_key" )
        auth_key_data = json.loads(response.text, 'utf8')
        password = auth_key_data["passwd_hash"]
        salt = auth_key_data["salt"]
        return password == hashlib.sha256(salt.encode() + input_password.encode()).hexdigest()


    def login_get( self, ):
        return bottle.template('login')

    def login_post( self, ):
        password = bottle.request.forms.get('password')
        if self.check_password( password) :
            logging.info( "Login")
            return "<p>Your login information was correct.</p>"
            #bottle.redirect("/")
        else:
            logging.info( "Login failed!")
            return "<p>Login failed.</p>"

#new_pass = input('Please enter a password: ')
#hashed_password = hash_password(new_pass)
#print('The string to store in the db is: ' + hashed_password)
#old_pass = input('Now please enter the password again to check: ')
#if check_password(hashed_password, old_pass):
    #print('You entered the right password')
#else:
    #print('I am sorry but the password does not match')
