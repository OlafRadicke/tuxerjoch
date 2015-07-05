import bottle
import json
import logging

import controls.article
import controls.auth
import controls.home
import controls.tags
import couch_backend.rest

class Tuxerjoch:

    def __init__(self):
        '''Constructor do some preparations for app environment'''
        self.app = bottle.Bottle()
        self.read_config()
        self.config_logger()
        self.config_database_connect()
        self.check_database_status()
        self.check_designs()
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
        '''Prepare database connect parameters for configuration'''
        self.couchDB = couch_backend.rest.RestWrapper()
        self.couchDB.setHost( self.config_data["couch_host"] )
        self.couchDB.setPort( self.config_data["couch_port"] )
        self.couchDB.setPassword( self.config_data["couch_passwd"] )
        self.couchDB.setUser( self.config_data["couch_user"] )
        self.couchDB.setDB( self.config_data["couch_db"] )

    def check_database_status(self):
        '''check and prepare database'''
        response = self.couchDB.getAllDBs()
        logging.debug( "Founded data bases: ")
        logging.debug( response.text )
        if self.config_data["couch_db"] in json.loads(response.text):
            logging.debug("I found database " + self.config_data["couch_db"])
        else:
            logging.info( "I can not found database " + self.config_data["couch_db"] + " and create now!")
            response = self.couchDB.createDB( self.config_data["couch_db"] )
            logging.info( response.text )

    def check_password_protection(self):
        '''check and prepare password protection'''
        response = self.couchDB.getDocValue( "auth_key" )
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

                response = self.couchDB.insertNamedDoc( "auth_key", json_code )
                logging.info( response.text )
            else:
                logging.error( "Unknown error: " )
                logging.error( auth_key_data["error"] + ": " + auth_key_data["reason"] )

    def check_designs( self ):
        '''Check and prepare designs'''
        response = self.couchDB.getDesignCode("blog_article")
        auth_key_data = json.loads(response.text, 'utf8')
        if "error" in auth_key_data:
            if auth_key_data["error"] == "not_found":
                logging.info( "Can not found designs / views and will create this now with defaults" )
                json_doc = '''{  \n
    "_id": "_design/blog_article", \n
    "language": "javascript", \n
    "views": { \n
        "all": {\n
            "map": "function(doc) { if (doc.document_type == 'blog_article')  emit(null, doc) }"\n
        },\n
        "all_tags": {\n
            "map": "function(doc) { \
                if (doc.document_type == 'blog_article') \
                for(var idx in doc.tags) \
                { emit('tag', doc.tags[idx])} }"\n
        }
    }\n
}'''
                logging.info(json_doc)
                response = self.couchDB.addNamedDesign( "blog_article", json_doc )
                logging.info(response.headers)
                logging.info(response.text)
            else:
                logging.error( "Unknown error: " )
                logging.error( auth_key_data["error"] + ": " + auth_key_data["reason"] )

    def static_file_get( self, filename ):
        '''Get back static content'''
        return bottle.static_file(filename, root='static')

    def pics_file_get( self, filename ):
        '''Get back static picture content'''
        return bottle.static_file(filename, root='static/pics')

    def bootstrap_file_get( self, filename ):
        '''Get back static pics content'''
        return bottle.static_file(filename, root='static/bootstrap/css')

    def init_controller(self):
        # init controller
        self.home_page           = controls.home.Home( self.couchDB )
        self.controllNewArticle  = controls.article.NewArticle( self.couchDB )
        self.controllViewArticle = controls.article.ViewArticle( self.couchDB )
        self.controllAuth        = controls.auth.Auth( self.couchDB )
        self.controllTags        = controls.tags.Tags( self.couchDB )

    def set_routs(self):
        '''set routs'''
        self.app.route('/bootstrap/css/<filename>', ['GET'], self.bootstrap_file_get)
        self.app.route('/pics/<filename>', ['GET'], self.pics_file_get)
        self.app.route('/static/<filename>', ['GET'], self.static_file_get)
        self.app.route('/', ['GET'],
                       self.home_page.start_get)
        self.app.route('/all_tags', ['GET'],
                       self.controllTags.all_tags_get)
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
        self.app.route('/tags/<tag_name>', ['GET'],
                       self.controllTags.tags_get)
        self.app.route('/view_article/<name>', ['GET'],
                       self.controllViewArticle.view_article_get)

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
