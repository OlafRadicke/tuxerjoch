import bottle
import json
import logging
import os.path
import datetime
import simplejson

import controls.article
import controls.articlemodify
import controls.atom_feed
import controls.auth
import controls.config
import controls.filemanagement
import controls.home
import controls.statistic
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
        self.check_password_protection()
        self.check_designs()
        self.check_tag_statistics()
        self.init_controler()
        self.set_routs()

    def read_config(self):
        '''Reade config file '''
        if os.path.isfile("tuxerjoch.conf"):
            with open("tuxerjoch.conf") as json_file:
                self.config_data = json.load(json_file)
        else:
            logging.debug("No local configuraton found. go continus with /etc/tuxerjoch.conf...")
            with open("/etc/tuxerjoch.conf") as json_file:
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
        response = self.couchDB.getDocValue( "global_config" )
        global_config_data = json.loads(response.text, 'utf8')
        if "error" in global_config_data:
            if global_config_data["error"] == "not_found":
                logging.info( "Can not found document global_config and create with default password" )
                json_code = '{ \n'
                json_code += '    "document_type": "app_config", \n'
                json_code += '    "passwd_hash": "613367845fd07938881688f6c7e222497d778db3c3d7ff85c764498347d495c9", \n'
                json_code += '    "salt": "tuxerjoch", \n'
                # signature key required for signed cookies
                json_code += '    "cookie_secret_key": "' + self.couchDB.getUUID() + '", \n'
                # cookie live time maximum age in seconds
                json_code += '    "cookie_live_time": 7200, \n'
                json_code += '    "result_sort_descending": "true", \n'
                json_code += '    "result_limit": 25, \n'
                json_code += '    "about_text": "Noch nicht gesetzt." \n'
                json_code += '}'

                response = self.couchDB.insertNamedDoc( "global_config", json_code )
                logging.info( response.text )
            else:
                logging.error( "Unknown error: " )
                logging.error( global_config_data["error"] + ": " + global_config_data["reason"] )
        else:
            # if section about_text not exist than set default
            if not "about_text" in global_config_data:
                logging.info( "Can not found section about_text and will create with default value" )
                global_config_data["about_text"] = "Noch nicht gesetzt"
            # if section statistic_report not exist than set default
            if not "statistic_report" in global_config_data:
                logging.info( "Can not found section statistic_report and will create with default value" )
                global_config_data["statistic_report"] = "/var/goaccess/the-independent-friend.de-access.log_report.html"

            response = self.couchDB.insertNamedDoc(
                "global_config",
                simplejson.dumps( global_config_data )
            )
            response_data = json.loads(response.text, 'utf8')
            if "error" in response_data:
                logging.error( response.text )
                return


            logging.info( "I found document global_config. Okay." )

    def check_designs( self ):
        '''Check and prepare designs'''
        response = self.couchDB.getDesignCode("blog_article")
        blog_article_desings = json.loads(response.text, 'utf8')
        if "error" in blog_article_desings:
            if blog_article_desings["error"] == "not_found":
                logging.info( "Can not found designs / views and will create this now with defaults" )
                self.create_design()
            else:
                logging.error( "Unknown error: " )
                logging.error( blog_article_desings["error"] + ": " + blog_article_desings["reason"] )
        else:
            logging.info( "Update default designs / views" )
            self.update_design(blog_article_desings)

    def update_design(self, blog_article_desings):
        rev = blog_article_desings["_rev"]
        json_doc = '''{  \n
    "_id": "_design/blog_article", \n
    "language": "javascript", \n
    "views": { \n
        "all": {\n
            "map": "function(doc) { if (doc.document_type == 'blog_article')  emit(doc.last_update, doc) }"\n
        },\n
        "draft_article": {\n
            "map": "function(doc) { if (doc.document_type == 'draft_article')  emit(doc.last_update, doc) }"\n
        },\n
        "all_tags": {\n
            "map": "function(doc) { \
                if (doc.document_type == 'blog_article') \
                for(var idx in doc.tags) \
                { emit('tag', doc.tags[idx])} }"\n
        }
    }\n
}'''
        jason_class = json.loads(json_doc)
        jason_class["_rev"] = rev
        json_doc = simplejson.dumps(jason_class)
        logging.info(json_doc)
        response = self.couchDB.addNamedDesign( "blog_article", json_doc )
        logging.info(response.headers)
        logging.info(response.text)



    def create_design(self):
        json_doc = '''{  \n
    "_id": "_design/blog_article", \n
    "language": "javascript", \n
    "views": { \n
        "all": {\n
            "map": "function(doc) { if (doc.document_type == 'blog_article')  emit(doc.last_update, doc) }"\n
        },\n
        "draft_article": {\n
            "map": "function(doc) { if (doc.document_type == 'draft_article')  emit(doc.last_update, doc) }"\n
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


    def check_tag_statistics( self ):
        '''Check and prepare tag_statistics document'''
        response = self.couchDB.getDocValue( "tag_statistics" )
        tag_statistics_data = json.loads(response.text, 'utf8')
        if "error" in tag_statistics_data:
            if tag_statistics_data["error"] == "not_found":
                logging.info( "Can not found tag statistic and will create this now with defaults" )
                current_time = datetime.datetime.now(datetime.timezone.utc)
                unix_timestamp = current_time.timestamp()
                json_code = '{ \n'
                json_code += '    "last_update": ' + str(unix_timestamp) + ', \n'
                json_code += '    "statistics": {} \n'
                json_code += '}'

                response = self.couchDB.insertNamedDoc( "tag_statistics", json_code )
                logging.debug(response.headers)
                logging.info( response.text )



    def static_file_get( self, filename ):
        '''Get back static content'''
        return bottle.static_file(filename, root='static')

    def pics_file_get( self, filename ):
        '''Get back static picture content'''
        return bottle.static_file(filename, root='static/pics')

    def bootstrap_file_get( self, filename ):
        '''Get back static pics content'''
        return bottle.static_file(filename, root='static/bootstrap/css')

    def init_controler(self):
        # init controler
        self.home_page             = controls.home.Home( self.couchDB )
        self.controlArticle       = controls.article.Article( self.couchDB )
        self.controlArticleModify = controls.articlemodify.ArticleModify( self.couchDB )
        self.controlAtom          = controls.atom_feed.Atom( self.couchDB, self.config_data )
        self.controlAuth          = controls.auth.Auth( self.couchDB )
        self.controlConf          = controls.config.Config( self.couchDB )
        self.controlFile          = controls.filemanagement.FileManagement( self.couchDB )
        self.controlStatistic     = controls.statistic.Statistic( self.couchDB )
        self.controlTags          = controls.tags.Tags( self.couchDB )

    def set_routs(self):
        '''set routs'''
        self.app.route('/bootstrap/css/<filename>', ['GET'], self.bootstrap_file_get)
        self.app.route('/pics/<filename>', ['GET'], self.pics_file_get)
        self.app.route('/static/<filename>', ['GET'], self.static_file_get)
        self.app.route('/', ['GET'],
                       self.home_page.start_get)
        self.app.route('/about', ['GET'],
                       self.home_page.about_get)
        self.app.route('/all_tags', ['GET'],
                       self.controlTags.all_tags_get)
        self.app.route('/atom.xml', ['GET'],
                       self.controlAtom.feed_get)
        self.app.route('/rss.xml', ['GET'],
                       self.controlAtom.rss_feed_get)
        self.app.route('/config', ['GET'],
                       self.controlConf.edit_get)
        self.app.route('/config', ['POST'],
                       self.controlConf.edit_post)
        self.app.route('/delete_article', ['POST'],
                       self.controlArticleModify.delete_post)
        self.app.route('/draft_queue', ['GET'],
                       self.home_page.draft_queue_get)
        self.app.route('/edit_article/<name>', ['GET'],
                       self.controlArticleModify.edit_get)
        self.app.route('/edit_article', ['POST'],
                       self.controlArticleModify.edit_post)
        self.app.route('/filedelete/<name>', ['GET'],
                       self.controlFile.filedelete_get)
        self.app.route('/filedelete/<name>', ['POST'],
                       self.controlFile.filedelete_post)
        self.app.route('/filemanagement', ['GET'],
                       self.controlFile.management_get)
        self.app.route('/filemanagement', ['POST'],
                       self.controlFile.upload_post)
        self.app.route('/edit_article/<name>', ['GET'],
                       self.controlArticleModify.edit_get)
        self.app.route('/login', ['GET'],
                       self.controlAuth.login_get)
        self.app.route('/login', ['POST'],
                       self.controlAuth.login_post)
        self.app.route('/logout', ['GET'],
                       self.controlAuth.logout_get)
        self.app.route('/new_article', ['GET'],
                       self.controlArticle.new_get)
        self.app.route('/new_article', ['POST'],
                       self.controlArticle.new_post)
        self.app.route('/statistic', ['GET'],
                       self.controlStatistic.statistic_get)
        self.app.route('/tags/<tag_name>', ['GET'],
                       self.controlTags.tags_get)
        self.app.route('/view_article/<name>', ['GET'],
                       self.controlArticle.view_article_get)



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
