# -*- coding: utf-8 -*-

import bottle
import json
import logging
import os.path

import controls.auth

class Statistic:

    def __init__(self, couchDB, ):
        self.couchDB = couchDB


    def statistic_get(self):
        '''This controller show the statistic'''
        authenticated = controls.auth.authenticated_check( self.couchDB )
        if authenticated == None:
            bottle.redirect("/login")

        global_config_data = json.loads( self.couchDB.getDocValue( "global_config" ).text, 'utf8')
        # check session
        authenticated = bottle.request.get_cookie("authenticated", secret = global_config_data["cookie_secret_key"])

        if os.path.isfile( global_config_data["statistic_report"] ):
            with open( global_config_data["statistic_report"] ) as html_statistic:
                print( html_statistic )
        else:
            logging.error( "Can not open " + global_config_data["statistic_report"])


            html_out = bottle.template(
                'skeleton',
                uri_prefix="../",
                title="Statistik",
                flashed_message="Can not open " + global_config_data["statistic_report"],
                flashed_level="danger",
                authenticated=authenticated)
            return html_out

        html_out = bottle.template(
            'skeleton',
            uri_prefix="../",
            title="Statistik",
            authenticated=authenticated,
            main_area=html_statistic)
        return html_out
