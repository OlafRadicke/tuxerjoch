# -*- coding: utf-8 -*-

import bottle
import json
import datetime
import uuid
import hashlib

class Auth:

    def __init__(self, couchDB):
        self.couchDB = couchDB


    def hash_password(password):
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
        # print( hashlib.sha256("tuxerjoch".encode() + tuxerjoch.encode()).hexdigest() + ':' + "tuxerjoch" )

    def check_password(hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


    def login_get():
        return bottle.template('login')

    def login_post():
        password = bottle.request.forms.get('password')
        if check_login(username, password):
            return "<p>Your login information was correct.</p>"
            bottle.redirect("/")
        else:
            return "<p>Login failed.</p>"

#new_pass = input('Please enter a password: ')
#hashed_password = hash_password(new_pass)
#print('The string to store in the db is: ' + hashed_password)
#old_pass = input('Now please enter the password again to check: ')
#if check_password(hashed_password, old_pass):
    #print('You entered the right password')
#else:
    #print('I am sorry but the password does not match')
