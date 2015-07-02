# -*- coding: utf-8 -*-

import bottle
import json
import datetime
import re
import logging

class NewArticle:

    def __init__(self, couchDB, ):
        self.couchDB = couchDB

    def new_get(self):
        auth_key_data = json.loads( self.couchDB.getDocValue( "auth_key" ).text, 'utf8')
        # check session
        authenticated = bottle.request.get_cookie("authenticated", secret = auth_key_data["cookie_secret_key"])
        if authenticated == None:
            bottle.redirect("/login")
        return bottle.template(
            'new_article',
            flashed_message=None,
            authenticated=authenticated)


    def new_post(self):
        '''This controller created a new article.'''
        auth_key_data = json.loads( self.couchDB.getDocValue( "auth_key" ).text, 'utf8')
        # check session
        authenticated = bottle.request.get_cookie("authenticated", secret = auth_key_data["cookie_secret_key"])
        if authenticated == None:
            bottle.redirect("/login")
        flashed_message = None
        uri_id = bottle.request.forms.getunicode('uri_id')
        title = bottle.request.forms.getunicode('title')
        article_text = bottle.request.forms.getunicode('article_text')
        tags = bottle.request.forms.getunicode('tags').lower()
        current_time = datetime.datetime.now(datetime.timezone.utc)
        unix_timestamp = current_time.timestamp()
        # extrahieren mit
        # nowstr = datetime.datetime.fromtimestamp( 1435737606.983997 )
        if (uri_id == None) or (uri_id == "" ):
            uri_id = self.couchDB.getUUID()
        else:
            uri_id = uri_id.lower()
            uri_id = uri_id.strip()
            # Remove special characters
            uri_id = re.sub('[^a-zA-Z0-9-_*.]', '', uri_id)
        uri_id = "articke_" + uri_id
        if (title == "") or (article_text == ""):
            return bottle.template(
                'new_article',
                flashed_message="Unvollständige Angaben!",
                authenticated=authenticated)
        else:
            #print( article_text )
            json_code = '{ \n'
            json_code += '"document_type": "blog_article", \n'
            json_code += '"uri_id": "' + uri_id + '", \n'
            json_code += '"title": "' + title + '", \n'
            json_code += '"article_text": "' + article_text + '", \n'
            json_code += '"created": ' + str(unix_timestamp) + ', \n'
            json_code += '"last_update": ' + str(unix_timestamp) + ', \n'
            json_code += '"tags": ["' + '","'.join( tags.split() ) + '"] \n'
            json_code += '}'

        logging.info( "Insert document: ")
        logging.info( json_code )
        response = self.couchDB.insertNamedDoc( uri_id, json_code )
        logging.info( response.text )
        bottle.redirect("/")


    def view_article_get(self, name):
        '''This controller show a article'''
        auth_key_data = json.loads( self.couchDB.getDocValue( "auth_key" ).text, 'utf8')
        # check session
        authenticated = bottle.request.get_cookie("authenticated", secret = auth_key_data["cookie_secret_key"])
        response = self.couchDB.getDocValue(name)
        logging.info( "view document: " )
        logging.info( name )
        logging.debug( response.text )
        artikle_data = json.loads(response.text, 'utf8')
        if "error" in artikle_data:
            if artikle_data["error"] == "not_found":
                return bottle.template(
                    'error',
                    authenticated=authenticated,
                    flashed_message="Dokument nicht gefunden!" )
            else:
                return bottle.template(
                    'error',
                    authenticated=authenticated,
                    flashed_message= artikle_data["error"] + ": " + artikle_data["reason"] )

        if "document_type" in artikle_data:
            if artikle_data["document_type"] != "blog_article":
                logging.error( "This document is not a blog article! Get a 401 error.")
                bottle.abort(401, "Sorry, access denied.")
        else:
            logging.error( "This document is not a blog article! Get a 401 error.")
            bottle.abort(401, "Sorry, access denied.")

        return bottle.template(
            'view_article',
            authenticated=authenticated,
            artikle=artikle_data)
