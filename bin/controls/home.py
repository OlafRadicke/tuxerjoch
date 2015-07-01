import bottle
import json

class Home:

    def __init__(self, couchDB):
        self.couchDB = couchDB

    def start_get(self):
        response = self.couchDB.getAllDocs()
        print( response.text )
        artikle_list = json.loads(response.text)
        #artikle_list = ['eins','zwei','drei']
        return bottle.template('home', artikles=artikle_list)
