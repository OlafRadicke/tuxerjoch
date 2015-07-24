# -*- coding: utf-8 -*-

import bottle
import json
import simplejson
import datetime
import re
import logging

import controls.auth

class Config:

    def __init__(self, couchDB, ):
        self.couchDB = couchDB

    def edit_get(self):
        '''The GET controller for creating new artikle page'''
        logging.info("-------INFO Test--------")
        logging.debug("-------DEBUG Test--------")
        logging.error("-------ERROR Test--------")


        authenticated = controls.auth.authenticated_check( self.couchDB )
        if authenticated == None:
            bottle.redirect("/login")

        global_config = json.loads( self.couchDB.getDocValue( "global_config" ).text, 'utf8')
        #if "about_text" in global_config_data:
            #about_text = global_config_data["about_text"]
        #else:
            #about_text = ""

        print(global_config)
        block_edit_config = bottle.template(
            'block_edit_config',
            global_config=global_config)

        html_code = bottle.template(
            'skeleton',
            title="Neuer Artikel",
            authenticated=authenticated,
            main_area=block_edit_config)
        return html_code


    def edit_post(self):
        '''The POST controller for creating new artikle page'''
        authenticated = controls.auth.authenticated_check( self.couchDB )
        if authenticated == None:
            bottle.redirect("/login")
        flashed_message = None

        global_config = json.loads( self.couchDB.getDocValue( "global_config" ).text, 'utf8')

        rev_id = bottle.request.forms.getunicode('rev_id')
        global_config["cookie_live_time"]  = int( bottle.request.forms.getunicode('cookie_live_time') )
        global_config["result_limit"]  = int( bottle.request.forms.getunicode('result_limit') )
        global_config["about_text"] = bottle.request.forms.getunicode('about_text')
        new_password = bottle.request.forms.getunicode('new_password')
        new_password_verify = bottle.request.forms.getunicode('new_password_verify')
        if new_password != "" and new_password_verify == new_password:
            salt = self.couchDB.getUUID()
            global_config["salt"] = salt
            global_config["passwd_hash"] = controls.auth.hash_password( new_password, salt )

        if new_password_verify != new_password:
            flashed_message = "Fehler bei der Passworteingabe (nicht gleich)"
            logging.error( flashed_message )
            block_edit_config = bottle.template(
                'block_edit_config',
                global_config=global_config)

            html_code = bottle.template(
                'skeleton',
                uri_prefix="../",
                title= "Konfiguration",
                flashed_message=flashed_message,
                flashed_level="danger",
                authenticated=authenticated,
                main_area=block_edit_config)
            return html_code


        logging.info( "I will insert document global_config : ")
        logging.info( simplejson.dumps( global_config ) )
        response = self.couchDB.insertNamedDoc(
            "global_config",
            simplejson.dumps( global_config ) )
        response_data = json.loads(response.text, 'utf8')
        if "error" in response_data:
            flashed_message = response_data["error"] + ": " + response_data["reason"]
            logging.error( response.text )
            block_edit_config = bottle.template(
                'block_edit_config',
                global_config=global_config)

            html_code = bottle.template(
                'skeleton',
                uri_prefix="../",
                title= "Konfiguration",
                flashed_message=flashed_message,
                flashed_level="danger",
                authenticated=authenticated,
                main_area=block_edit_config)
            return html_code
        else:
            flashed_message = "Änderungen wurden gespeichert"
            logging.info( "Änderungen wurden gespeichert" )
            logging.info( response.text )
            block_edit_config = bottle.template(
                'block_edit_config',
                global_config=global_config)

            html_code = bottle.template(
                'skeleton',
                uri_prefix="../",
                title= "Konfiguration",
                flashed_message=flashed_message,
                flashed_level="success",
                authenticated=authenticated,
                main_area=block_edit_config)
            return html_code

