import bottle
import json
import logging

import controls.auth

class Home:

    def __init__(self, couchDB):
        self.couchDB = couchDB

    def start_get(self):
        '''Controller of the start page'''
        authenticated = controls.auth.authenticated_check( self.couchDB )
        response = self.couchDB.getNamedView( "blog_article", "all?descending=true&limit=25")
        artikle_list = json.loads(response.text)
        if "error" in artikle_list:
            logging.info( response.text )

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
