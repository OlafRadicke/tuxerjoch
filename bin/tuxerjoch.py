import bottle
import json
import logging

import controls.article
import controls.auth
import controls.home
import couch_backend.rest

class Tuxerjoch:

    def __init__(self):
        '''Constructor do some preparations for app environment'''
        self.app = bottle.Bottle()
        self.read_config()
        self.config_logger()
        self.config_database_connect()
        self.check_database_status()
        self.init_controller()
        self.set_routs()

    def read_config(self):
        '''Reade config file '''
        with open("tuxerjoch.conf") as json_file:
            self.config_data = json.load(json_file)

    def config_logger(self):
        '''Prepare logger'''
        if self.config_data["log_level"] == "DEBUG":
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s %(name)-2s %(levelname)-2s %(message)s',
                datefmt='%m-%d %H:%M',
                filename=self.config_data["log_file"],
                filemode='w'
            )
        if self.config_data["log_level"] == "INFO":
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename=self.config_data["log_file"],
                filemode='w'
            )
        if self.config_data["log_level"] == "ERROR":
            logging.basicConfig(
                level=logging.ERROR,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename=self.config_data["log_file"],
                filemode='w'
            )

    def config_database_connect(self):
        '''Prepare database connect'''
        self.restWrapper = couch_backend.rest.RestWrapper()
        self.restWrapper.setHost( self.config_data["couch_host"] )
        self.restWrapper.setPort( self.config_data["couch_port"] )
        self.restWrapper.setPassword( self.config_data["couch_passwd"] )
        self.restWrapper.setUser( self.config_data["couch_user"] )
        self.restWrapper.setDB( self.config_data["couch_db"] )

    def check_database_status(self):
        '''check database'''
        response = self.restWrapper.getAllDBs()
        logging.debug( "Founded data bases: ")
        logging.debug( response.text )
        if self.config_data["couch_db"] in json.loads(response.text):
            logging.debug("I found database " + self.config_data["couch_db"])
        else:
            logging.info( "I can not found database " + self.config_data["couch_db"] + " and create now!")
            response = self.restWrapper.createDB( self.config_data["couch_db"] )
            logging.info( response.text )

    def check_password_protection(self):
        '''check password protection'''
        response = self.restWrapper.getDocValue( "auth_key" )
        print( response.text )
        auth_key_data = json.loads(response.text, 'utf8')
        if "error" in auth_key_data:
            if auth_key_data["error"] == "not_found":
                logging.info( "Can not found document auth_key and create with default password" )
                json_code = '{ \n'
                json_code += '    "document_type": "app_config", \n'
                json_code += '    "passwd_hash": "613367845fd07938881688f6c7e222497d778db3c3d7ff85c764498347d495c9", \n'
                json_code += '    "salt": "tuxerjoch", \n'
                # signature key required for signed cookies
                json_code += '    "cookie_secret_key": "tuxerjoch", \n'
                # cookie live time maximum age in seconds
                json_code += '    "cookie_live_time": 7200 \n'
                json_code += '}'

                response = self.restWrapper.insertNamedDoc( "auth_key", json_code )
                logging.info( response.text )
            else:
                logging.error( "Unknown error: " )
                logging.error( auth_key_data["error"] + ": " + auth_key_data["reason"] )



    def static_file_get( self, filename ):
        '''Get back static content'''
        return bottle.static_file(filename, root='static')

    def pics_file_get( self, filename ):
        '''Get back static picture content'''
        print("Search pic: " + filename)
        return bottle.static_file(filename, root='static/pics')

    def bootstrap_file_get( self, filename ):
        '''Get back static pics content'''
        print("Search pic: " + filename)
        return bottle.static_file(filename, root='static/bootstrap/css')

    def init_controller(self):
        # init controller
        self.home_page          = controls.home.Home( self.restWrapper )
        self.controllNewArticle = controls.article.NewArticle( self.restWrapper )
        self.controllAuth       = controls.auth.Auth( self.restWrapper )

    def set_routs(self):
        '''set routs'''
        self.app.route('/bootstrap/css/<filename>', ['GET'], self.bootstrap_file_get)
        self.app.route('/pics/<filename>', ['GET'], self.pics_file_get)
        self.app.route('/static/<filename>', ['GET'], self.static_file_get)
        self.app.route('/', ['GET'],
                       self.home_page.start_get)
        self.app.route('/login', ['GET'],
                       self.controllAuth.login_get)
        self.app.route('/login', ['POST'],
                       self.controllAuth.login_post)
        self.app.route('/logout', ['GET'],
                       self.controllAuth.logout_get)
        self.app.route('/new_article', ['GET'],
                       self.controllNewArticle.new_get)
        self.app.route('/new_article', ['POST'],
                       self.controllNewArticle.new_post)
        self.app.route('/view_article/<name>', ['GET'],
                       self.controllNewArticle.view_article_get)

    def run(self):
        '''Start listening'''
        bottle.run(
            self.app,
            host=self.config_data["webservice_host"],
            port=self.config_data["webservice_port"],
            server='cherrypy'
            )

tuxerjoch = Tuxerjoch()
tuxerjoch.run()
