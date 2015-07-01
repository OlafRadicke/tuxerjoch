# -*- coding: utf-8 -*-

import bottle
import json
import datetime
import re

class NewArticle:

    def __init__(self, couchDB):
        self.couchDB = couchDB

    def new_get(self):
        return bottle.template('new_article', flashed_message=None)


    def new_post(self):
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
        if (title == "") or (article_text == ""):
            return bottle.template('new_article', flashed_message="Unvollständige Angaben!" )
        else:
            #dataSet = dict()
            #dataSet["document_type"] = "blog_article"
            #dataSet["uri_id"] = uri_id
            #dataSet["title"] = title
            #dataSet["article_text"] = article_text
            #dataSet["created"] = unix_timestamp
            #dataSet["last_update"] = unix_timestamp
            #dataSet["tags"] = tags.split()

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

        #json_code = json.dumps( dataSet )
        print( json_code )
        response = self.couchDB.insertNamedDoc( uri_id, json_code )
        print( response.text )
        bottle.redirect("/")


    def view_article_get(self, name):
        response = self.couchDB.getDocValue(name)
        print( response.text )
        artikle_data = json.loads(response.text, 'utf8')
        return bottle.template('view_article', artikle=artikle_data)
