import bottle
import json

class Home:

    def __init__(self, couchDB):
        self.couchDB = couchDB

    def start_get(self):
        '''Controller of the start page'''
        auth_key_data = json.loads( self.couchDB.getDocValue( "auth_key" ).text, 'utf8')
        # check session
        authenticated = bottle.request.get_cookie("authenticated", secret = auth_key_data["cookie_secret_key"])

        response = self.couchDB.getAllDocs()
        artikle_list = json.loads(response.text)
        return bottle.template(
            'home',
            authenticated=authenticated,
            artikles=artikle_list
        )
