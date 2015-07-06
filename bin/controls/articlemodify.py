# -*- coding: utf-8 -*-

import bottle
import json
import simplejson
import datetime
import re
import logging

import controls.auth

class ArticleModify:

    def __init__(self, couchDB, ):
        self.couchDB = couchDB

    def delete_post( self ):
        '''Delete a article'''
        # ACL check
        authenticated = controls.auth.authenticated_check( self.couchDB )
        if authenticated == None:
            bottle.redirect("/login")
        rev_id = bottle.request.forms.getunicode('rev_id')
        uri_id = bottle.request.forms.getunicode('uri_id')

        logging.info( "Deltet article " + uri_id )
        response = self.couchDB.deleteDoc( uri_id )
        response_data = json.loads(response.text, 'utf8')

        if "error" in response_data:
            flashed_message = artikle_data["error"] + ": " + artikle_data["reason"]
            logging.error( flashed_message )

            block_error = bottle.template(
                'block_error',
                flashed_message="flashed_message!" )

            html_code = bottle.template(
                'skeleton',
                uri_prefix="../",
                title= "Artikellöschung",
                authenticated=authenticated,
                main_area=block_error)
        else:
            logging.info( response.text )
            html_code = bottle.template(
                'skeleton',
                uri_prefix="../",
                title= "Artikellöschung",
                authenticated=authenticated,
                main_area="<h1>Artikel gelöscht!</h1>")

        return html_code


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

            logging.error( artikle_data["error"] + ": " + artikle_data["reason"] )
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
        created = bottle.request.forms.getunicode('created')
        rev_id = bottle.request.forms.getunicode('rev_id')
        uri_id = bottle.request.forms.getunicode('uri_id')
        title = bottle.request.forms.getunicode('title')
        teaser_text = simplejson.dumps(  bottle.request.forms.getunicode('teaser_text') )
        article_text = simplejson.dumps(  bottle.request.forms.getunicode('article_text') )
        tags = bottle.request.forms.getunicode('tags').lower()
        current_time = datetime.datetime.now(datetime.timezone.utc)
        unix_timestamp = current_time.timestamp()

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
        artikle_data = json.loads( json_code, 'utf8')

        if bottle.request.forms.getunicode('delete') :
            block_delete_article = bottle.template(
                'block_delete_article',
                artikle=artikle_data )

            html_code = bottle.template(
                'skeleton',
                title="Artikel löschen",
                flashed_level="warning",
                flashed_message="Artikel wirklich löschen?!",
                authenticated=authenticated,
                main_area=block_delete_article)
            return html_code

        if (title == "") or (article_text == "") or (teaser_text == ""):
            block_edit_article = bottle.template(
                'block_edit_article',
                artikle=artikle_data )

            return bottle.template(
                'skeleton',
                title="Neuer Artikel",
                flashed_level="warning",
                flashed_message="Unvollständige Angaben!",
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

        if bottle.request.forms.getunicode('save') == "true":
            response = self.couchDB.insertNamedDoc( uri_id, json_code )
            response_data = json.loads(response.text, 'utf8')
            if "error" in response_data:
                flashed_message = response_data["error"] + ": " + response_data["reason"]
                logging.error( response.text )
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



