import bottle
import json
import logging

import controls.auth

class Atom:

    def __init__(self, couchDB, config_data):
        self.couchDB = couchDB
        self.config_data = config_data

    def feed_get(self):
        '''Controller of the atom feed page'''
        global_config_data = json.loads( self.couchDB.getDocValue( "global_config" ).text, 'utf8')
        response = self.couchDB.getNamedView(
            "blog_article",
            "all?descending=true&limit=" + str(global_config_data["result_limit"]) )
        artikle_list = json.loads(response.text)
        if "error" in artikle_list:
            logging.error( response.text )

        response.content_type = 'text/html'
        html_sources = bottle.template(
            'atom',
            artikles=artikle_list["rows"],
            hostname=self.config_data["webservice_host"]
        )
        return html_sources


    def rss_feed_get(self):
        '''Controller of the atom feed page'''
        global_config_data = json.loads( self.couchDB.getDocValue( "global_config" ).text, 'utf8')
        response = self.couchDB.getNamedView(
            "blog_article",
            "all?descending=true&limit=" + str(global_config_data["result_limit"]) )
        artikle_list = json.loads(response.text)
        if "error" in artikle_list:
            logging.error( response.text )

        response.content_type = 'text/html'
        html_sources = bottle.template(
            'rss',
            artikles=artikle_list["rows"],
            hostname=self.config_data["webservice_host"]
        )
        return html_sources
