# -*- coding: utf-8 -*-

import bottle
import json
import simplejson
import datetime
import re
import logging

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

        block_filemanagement = bottle.template(
            'block_filemanagement',
            flashed_message=None)

        return bottle.template(
            'skeleton',
            title="Bildverwaltung",
            authenticated=authenticated,
            main_area=block_filemanagement)



    def upload_post(self):
        '''The POST controller for creating new artikle page'''
        authenticated = controls.auth.authenticated_check( self.couchDB )
        if authenticated == None:
            bottle.redirect("/login")

        file_id = bottle.request.forms.get('file_id')
        upload = bottle.request.files.get('upload')
#        name, ext = os.path.splitext(upload.filename)
        #if ext not in ('.png','.jpg','.jpeg'):
            #return 'File extension not allowed.'

#        save_path = get_save_path_for_category(category)
        print ( file_id )
        upload.save( "./static/pics/" + file_id, overwrite=True)

        #bottle.redirect("/filemanagement")


        block_filemanagement = bottle.template(
            'block_filemanagement')

        return bottle.template(
            'skeleton',
            title="Bildverwaltung",
            authenticated=authenticated,
            flashed_level="success",
            flashed_message="Datei gespeichert",
            main_area=block_filemanagement)


