import bottle
import json

import controls.auth

class Home:

    def __init__(self, couchDB):
        self.couchDB = couchDB

    def start_get(self):
        '''Controller of the start page'''
        authenticated = controls.auth.authenticated_check( self.couchDB )
        response = self.couchDB.getNamedView( "blog_article", "all")
        artikle_list = json.loads(response.text)
        block_article_list = bottle.template(
            'block_article_list',
            artikles=artikle_list
        )
        html_sources = bottle.template(
            'skeleton',
            title="Startseite",
            authenticated=authenticated,
            main_area=block_article_list
        )
        return html_sources
