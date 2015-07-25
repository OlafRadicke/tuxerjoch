# -*- coding: utf-8 -*-

import bottle
import json
import simplejson
import datetime
import re
import logging
import os

import controls.auth

class FileManagement:

    def __init__(self, couchDB, ):
        self.couchDB = couchDB


    def management_get(self):
        '''The GET controller for file management page'''
        authenticated = controls.auth.authenticated_check( self.couchDB )
        #authenticated = self.authenticated_check()
        if authenticated == None:
            bottle.redirect("/login")

        for dirname, dirnames, filenames in os.walk('./static/pics/'):
            pass

        block_filemanagement = bottle.template(
            'block_filemanagement',
            filenames=filenames)

        return bottle.template(
            'skeleton',
            uri_prefix="../",
            title="Bildverwaltung",
            authenticated=authenticated,
            main_area=block_filemanagement)



    def upload_post(self):
        '''The POST controller for file upload page'''
        authenticated = controls.auth.authenticated_check( self.couchDB )
        if authenticated == None:
            bottle.redirect("/login")

        file_id = bottle.request.forms.get('file_id')
        upload = bottle.request.files.get('upload')

        for dirname, dirnames, filenames in os.walk('./static/pics/'):
            if file_id in filenames:
                block_filemanagement = bottle.template(
                    'block_filemanagement',
                    filenames=filenames)

                html_code = bottle.template(
                    'skeleton',
                    uri_prefix="../",
                    title="Bildverwaltung",
                    authenticated=authenticated,
                    flashed_level="warning",
                    flashed_message="Es existiert schon eine Datei mit diesem Namen!",
                    main_area=block_filemanagement)
                return html_code
                
        upload.save( "./static/pics/" + file_id, overwrite=False)

        for dirname, dirnames, filenames in os.walk('./static/pics/'):
            pass

        block_filemanagement = bottle.template(
            'block_filemanagement',
            filenames=filenames)

        return bottle.template(
            'skeleton',
            uri_prefix="../",
            title="Bildverwaltung",
            authenticated=authenticated,
            flashed_level="success",
            flashed_message="Datei gespeichert",
            main_area=block_filemanagement)


    def filedelete_get(self, name):
        '''The GET controller for delete file page'''
        authenticated = controls.auth.authenticated_check( self.couchDB )
        if authenticated == None:
            bottle.redirect("/login")

        block_deltefile = bottle.template(
            'block_deltefile',
            filename=name)

        return bottle.template(
            'skeleton',
            uri_prefix="../",
            title="Bildverwaltung",
            authenticated=authenticated,
            main_area=block_deltefile)



    def filedelete_post(self, name):
        '''The POST controller for delete file page'''
        authenticated = controls.auth.authenticated_check( self.couchDB )
        if authenticated == None:
            bottle.redirect("/login")

        filename = bottle.request.forms.getunicode('filename')
        if filename == None or filename == '' and filename != name:
            level="warning"
            message="Fehlerhafter Seitenaufruf!"
        else:
            os.remove('./static/pics/' + filename)
            level="success"
            message="Datei wurde gelöscht"

        for dirname, dirnames, filenames in os.walk('./static/pics/'):
            pass

        block_filemanagement = bottle.template(
            'block_filemanagement',
            filenames=filenames)

        return bottle.template(
            'skeleton',
            uri_prefix="../",
            title="Bildverwaltung",
            authenticated=authenticated,
            flashed_level=level,
            flashed_message=message,
            main_area=block_filemanagement)
