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
        uri_id = bottle.request.forms.get('uri_id')
        title = bottle.request.forms.get('title')
        article_text = bottle.request.forms.get('article_text')
        tags = bottle.request.forms.get('tags').lower()
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
            dataSet = dict()
            dataSet["document_type"] = "blog_article"
            dataSet["uri_id"] = uri_id
            dataSet["title"] = title
            dataSet["article_text"] = article_text
            dataSet["created"] = unix_timestamp
            dataSet["last_update"] = unix_timestamp
            dataSet["tags"] = tags.split()

        print( json.dumps( dataSet ) )
        self.couchDB.insertDoc( json.dumps( dataSet ) )
        bottle.redirect("/")
