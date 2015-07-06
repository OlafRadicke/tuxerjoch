# -*- coding: utf-8 -*-

import bottle
import json
import simplejson
import datetime
import re
import logging

import controls.auth

class Tags:

    def __init__(self, couchDB, ):
        self.couchDB = couchDB


    def tags_get( self, tag_name ):
        '''lists all the article with a named tag'''
        global_config_data = json.loads( self.couchDB.getDocValue( "global_config" ).text, 'utf8')
        authenticated = bottle.request.get_cookie("authenticated", secret = global_config_data["cookie_secret_key"])
        json_request =  '{'
        json_request +=     '"map" : "function(doc) { '
        json_request +=         'if( '
        json_request +=             'doc.document_type == \'blog_article\' '
        json_request +=             '&& doc.tags.indexOf(\'' + tag_name + '\')  !== -1 '
        json_request +=         ') { '
        json_request +=             'emit(\'title\', doc.title); '
        json_request +=         '} '
        json_request +=      '}" '
        json_request +=  '} '
        response = self.couchDB.getTempView( json_request )
        article_of_tag = artikle_data = json.loads( response.text, 'utf8' )

        block_article_of_tag = bottle.template(
            'block_tags',
            tag_name=tag_name,
            article_of_tag=article_of_tag)

        return bottle.template(
            'skeleton',
            uri_prefix="../",
            title="Schlagwort" + tag_name,
            authenticated=authenticated,
            main_area=block_article_of_tag)


    def all_tags_get( self ):
        '''show all used tags'''
        global_config_data = json.loads( self.couchDB.getDocValue( "global_config" ).text, 'utf8')
        authenticated = bottle.request.get_cookie("authenticated", secret = global_config_data["cookie_secret_key"])
        '''check and prepare password protection'''
        response = self.couchDB.getDocValue( "tag_statistics" )
        tag_statistics = json.loads(response.text, 'utf8')
        if "error" in tag_statistics:
            if tag_statistics["error"] == "not_found":
                logging.info( "Can not found document tag_statistics and create with default password" )
                json_code = self.gen_json_tag_statistics()
                tag_statistics = json.loads( json_code, 'utf8')
                response = self.couchDB.insertNamedDoc( "tag_statistics", json_code )
                response_data = json.loads(response.text, 'utf8')
                if "error" in tag_statistics:
                    flashed_message = response_data["error"] + ": " + response_data["reason"]
                    logging.error( flashed_message )
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
            else:
                flashed_message = tag_statistics["error"] + ": " + tag_statistics["reason"]
                logging.error( flashed_message )
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
            current_time = datetime.datetime.now(datetime.timezone.utc)
            unix_timestamp = current_time.timestamp()
            '''if document older than 30 seconds (end of live)'''
            print( str( tag_statistics["last_update"] ) + " < " + str( ( unix_timestamp - 30 ) ) )
            if tag_statistics["last_update"] < ( unix_timestamp - 30 ) :
                logging.info( "The tag statistics document is older than 30 seconds (end of live). Refresh document now." )
                json_code = self.gen_json_tag_statistics( tag_statistics["_rev"] )
                tag_statistics = json.loads( json_code, 'utf8')
                response = self.couchDB.insertNamedDoc( "tag_statistics", json_code )
                response_data = json.loads(response.text, 'utf8')
                if "error" in tag_statistics:
                    flashed_message = response_data["error"] + ": " + response_data["reason"]
                    logging.error( flashed_message )
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
                    logging.info( "Updated the tag statistics document:" )
                    logging.info( response.text )
            else:
                logging.info( "The tag statistics document is up to date" )

            logging.info( response.text )
            block_view_all_tags = bottle.template(
                'block_view_all_tags',
                tag_statistics=tag_statistics)

            html_code = bottle.template(
                'skeleton',
                uri_prefix="../",
                title="Schlagworte",
                authenticated=authenticated,
                main_area=block_view_all_tags)
            return html_code


    def gen_json_tag_statistics( self, rev_id ):
        '''Generate a tag statistic in json formatted'''
        current_time = datetime.datetime.now(datetime.timezone.utc)
        unix_timestamp = current_time.timestamp()
        response = self.couchDB.getNamedView( "blog_article", "all_tags")
        tag_statistics = dict()
        for item in json.loads(response.text)["rows"]:
            if item["value"] in tag_statistics.keys():
                tag_statistics[item["value"]] += 1
            else:
                tag_statistics[item["value"]] = 1
        json_code = '{ \n'
        json_code += '    "_rev": "' + rev_id + '", \n'
        json_code += '    "last_update": ' + str(unix_timestamp) + ', \n'
        json_code += '    "statistics": ' + simplejson.dumps( tag_statistics)  + ' \n'
        json_code += '}'
        return json_code

