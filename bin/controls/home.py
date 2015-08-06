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
        global_config_data = json.loads( self.couchDB.getDocValue( "global_config" ).text, 'utf8')
        response = self.couchDB.getNamedView(
            "blog_article",
            "all?descending=true&limit=" + str(global_config_data["result_limit"]) )
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


    def draft_queue_get(self):
        '''Controller of the article draft queue.'''
        authenticated = controls.auth.authenticated_check( self.couchDB )
        if authenticated == None:
            bottle.redirect("/login")


        global_config_data = json.loads( self.couchDB.getDocValue( "global_config" ).text, 'utf8')
        response = self.couchDB.getNamedView(
            "blog_article",
            "draft_article?descending=true&limit=" + str(global_config_data["result_limit"]) )
        artikle_list = json.loads(response.text)
        if "error" in artikle_list:
            logging.info( response.text )

        block_draft_list = bottle.template(
            'block_draft_list',
            artikles=artikle_list
        )
        html_sources = bottle.template(
            'skeleton',
            title="Startseite",
            authenticated=authenticated,
            main_area=block_draft_list
        )
        return html_sources


    def about_get(self):
        '''Controller of the start page'''
        authenticated = controls.auth.authenticated_check( self.couchDB )
        global_config_data = json.loads( self.couchDB.getDocValue( "global_config" ).text, 'utf8')
        #if "about_text" in global_config_data:
            #about_text = global_config_data["about_text"]
        #else:
            #about_text = ""

        html_sources = bottle.template(
            'skeleton',
            title="Impressum",
            authenticated=authenticated,
            main_area=global_config_data["about_text"]
        )
        return html_sources
