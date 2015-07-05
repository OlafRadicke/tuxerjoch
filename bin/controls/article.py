# -*- coding: utf-8 -*-

import bottle
import json
import simplejson
import datetime
import re
import logging

import controls.auth

class Article:

    def __init__(self, couchDB, ):
        self.couchDB = couchDB


    def new_get(self):
        '''The GET controller for creating new artikle page'''
        authenticated = controls.auth.authenticated_check( self.couchDB )
        #authenticated = self.authenticated_check()
        if authenticated == None:
            bottle.redirect("/login")

        block_new_article = bottle.template(
            'block_new_article',
            flashed_message=None)

        return bottle.template(
            'skeleton',
            title="Neuer Artikel",
            authenticated=authenticated,
            main_area=block_new_article)



    def new_post(self):
        '''The POST controller for creating new artikle page'''
        authenticated = controls.auth.authenticated_check( self.couchDB )
        if authenticated == None:
            bottle.redirect("/login")
        flashed_message = None
        uri_id = bottle.request.forms.getunicode('uri_id')
        title = bottle.request.forms.getunicode('title')
        teaser_text = simplejson.dumps(  bottle.request.forms.getunicode('teaser_text') )
        article_text = simplejson.dumps(  bottle.request.forms.getunicode('article_text') )
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
        uri_id = "blog_articel_" + uri_id
        if (title == "") or (article_text == "") or (teaser_text == ""):
            block_new_article = bottle.template(
                'block_new_article',
                flashed_message="Unvollständige Angaben!")

            return bottle.template(
                'skeleton',
                title="Neuer Artikel",
                authenticated=authenticated,
                main_area=block_new_article)

        else:
            #print( article_text )
            json_code = '{ \n'
            json_code += '"document_type": "blog_article", \n'
            json_code += '"uri_id": "' + uri_id + '", \n'
            json_code += '"title": "' + title + '", \n'
            json_code += '"teaser": ' + teaser_text + ', \n'
            json_code += '"article_text": ' + article_text + ', \n'
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
                flashed_message="Dokument nicht gefunden!"
            else:
                flashed_message= artikle_data["error"] + ": " + artikle_data["reason"]

            block_error = bottle.template(
                'block_error',
                flashed_message="Dokument nicht gefunden!" )

            return bottle.template(
                'skeleton',
                uri_prefix="../",
                title=artikle_data["title"],
                authenticated=authenticated,
                main_area=block_error)

        # Do you show only blog article. Nothing else!
        if "document_type" in artikle_data:
            if artikle_data["document_type"] != "blog_article":
                logging.error( "This document is not a blog article! Get a 401 error.")
                bottle.abort(401, "Sorry, access denied.")
        else:
            logging.error( "This document is not a blog article! Get a 401 error.")
            bottle.abort(401, "Sorry, access denied.")

        block_view_article = bottle.template(
            'block_view_article',
            authenticated=authenticated,
            artikle=artikle_data)

        return bottle.template(
            'skeleton',
            uri_prefix="../",
            title=artikle_data["title"],
            authenticated=authenticated,
            main_area=block_view_article)


    def edit_get(self, name):
        '''The GET controller for edit a artikle'''
        # ACL check
        authenticated = controls.auth.authenticated_check( self.couchDB )
        if authenticated == None:
            bottle.redirect("/login")

        response = self.couchDB.getDocValue(name)
        logging.info( "view document: " )
        logging.info( name )
        logging.debug( response.text )
        artikle_data = json.loads(response.text, 'utf8')
        if "error" in artikle_data:
            if artikle_data["error"] == "not_found":
                flashed_message="Dokument nicht gefunden!"
            else:
                flashed_message= artikle_data["error"] + ": " + artikle_data["reason"]

            block_error = bottle.template(
                'block_error',
                flashed_message="Dokument nicht gefunden!" )

            html_code = bottle.template(
                'skeleton',
                uri_prefix="../",
                title= "Artikel bearbeiten",
                authenticated=authenticated,
                main_area=block_error)
            return html_code

        print(artikle_data)
        block_edit_article = bottle.template(
            'block_edit_article',
            artikle=artikle_data )

        html_code = bottle.template(
            'skeleton',
            uri_prefix="../",
            title= "Artikel bearbeiten",
            authenticated=authenticated,
            main_area=block_edit_article)
        return html_code

    def edit_post(self):
        '''The POST controller for edit a artikle'''
        # ACL check
        authenticated = controls.auth.authenticated_check( self.couchDB )
        if authenticated == None:
            bottle.redirect("/login")

        flashed_message = None
        print("if delete?")
        print(bottle.request.forms.getunicode('delete'))

        created = bottle.request.forms.getunicode('created')
        rev_id = bottle.request.forms.getunicode('rev_id')
        uri_id = bottle.request.forms.getunicode('uri_id')
        title = bottle.request.forms.getunicode('title')
        teaser_text = simplejson.dumps(  bottle.request.forms.getunicode('teaser_text') )
        article_text = simplejson.dumps(  bottle.request.forms.getunicode('article_text') )
        tags = bottle.request.forms.getunicode('tags').lower()
        current_time = datetime.datetime.now(datetime.timezone.utc)
        unix_timestamp = current_time.timestamp()
        # extrahieren mit
        # nowstr = datetime.datetime.fromtimestamp( 1435737606.983997 )

        if (title == "") or (article_text == "") or (teaser_text == ""):
            block_new_article = bottle.template(
                'block_new_article',
                flashed_message="Unvollständige Angaben!")

            return bottle.template(
                'skeleton',
                title="Neuer Artikel",
                authenticated=authenticated,
                main_area=block_new_article)

        else:
            #print( article_text )
            json_code = '{ \n'
            json_code += '"_rev": "' + rev_id + '", \n'
            json_code += '"document_type": "blog_article", \n'
            json_code += '"uri_id": "' + uri_id + '", \n'
            json_code += '"title": "' + title + '", \n'
            json_code += '"teaser": ' + teaser_text + ', \n'
            json_code += '"article_text": ' + article_text + ', \n'
            json_code += '"created": ' + created + ', \n'
            json_code += '"last_update": ' + str(unix_timestamp) + ', \n'
            json_code += '"tags": ["' + '","'.join( tags.split() ) + '"] \n'
            json_code += '}'

        logging.info( "Insert document: ")
        logging.info( json_code )

        print("if save?")
        print(bottle.request.forms.getunicode('save'))
        if bottle.request.forms.getunicode('save') == "true":
            response = self.couchDB.insertNamedDoc( uri_id, json_code )
            response_data = json.loads(response.text, 'utf8')
            if "error" in response_data:
                flashed_message = response_data["error"] + ": " + response_data["reason"]
                logging.info( response.text )
                block_error = bottle.template(
                    'block_error',
                    flashed_message=flashed_message )

                html_code = bottle.template(
                    'skeleton',
                    uri_prefix="../",
                    title= "Fehler",
                    authenticated=authenticated,
                    main_area=block_error)
                return html_code
            else:
                logging.info( response.text )
                bottle.redirect("/")



