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


    def check_password( self, input_password ):
        response = self.couchDB.getDocValue( "global_config" )
        global_config_data = json.loads(response.text, 'utf8')
        password = global_config_data["passwd_hash"]
        salt = global_config_data["salt"]
        return password == hashlib.sha256(salt.encode() + input_password.encode()).hexdigest()


    def login_get( self, ):
        '''Controller function for get login method'''
        global_config_data = json.loads( self.couchDB.getDocValue( "global_config" ).text, 'utf8')
        authenticated = bottle.request.get_cookie(
            "authenticated",
            secret = global_config_data["cookie_secret_key"]
        )
        if authenticated == "true":
            bottle.redirect("/")

        block_login = bottle.template(
            'block_login',
            flashed_message=None
        )

        return bottle.template(
            'skeleton',
            title="Login",
            authenticated=authenticated,
            main_area=block_login)


    def login_post( self, ):
        '''Controller function for post login method'''
        password = bottle.request.forms.get('password')
        if self.check_password( password) :
            logging.info( "Login session")
            global_config_data = json.loads( self.couchDB.getDocValue( "global_config" ).text, 'utf8')
            bottle.response.set_cookie(
                "authenticated",
                "true",
                secret = global_config_data["cookie_secret_key"],
                max_age = global_config_data["cookie_live_time"]
            )
            #return "<p>Your login information was correct.</p>"
            bottle.redirect("/")
        else:
            logging.info( "Login failed!")
            return "<p>Login failed.</p>"
            return bottle.template(
                'login',
                flashed_message="Login fehlgeschlagen!" ,
                authenticated=authenticated)



    def logout_get( self, ):
        '''Controller function for get logout method'''
        global_config_data = json.loads( self.couchDB.getDocValue( "global_config" ).text, 'utf8')
        bottle.response.set_cookie(
            "authenticated",
            None,
            secret = global_config_data["cookie_secret_key"]
        )
        bottle.redirect("/")

def authenticated_check( couchDB ):
    '''Checked is the user authenticated and return the result'''
    global_config_data = json.loads( couchDB.getDocValue( "global_config" ).text, 'utf8')
    # check session
    authenticated = bottle.request.get_cookie(
        "authenticated",
        secret = global_config_data["cookie_secret_key"])
    return authenticated

def hash_password( password, salt ):
    return hashlib.sha256( salt.encode() + password.encode() ).hexdigest()
