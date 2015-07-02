import bottle
import json
import logging

import controls.article
import controls.auth
import controls.home
import couch_backend.rest

app = bottle.Bottle()


# Reade config file
with open("tuxerjoch.conf") as json_file:
    config_data = json.load(json_file)

# prepare logger
if config_data["log_level"] == "DEBUG":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)-2s %(levelname)-2s %(message)s',
        datefmt='%m-%d %H:%M',
        filename=config_data["log_file"],
        filemode='w'
    )
if config_data["log_level"] == "INFO":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M',
        filename=config_data["log_file"],
        filemode='w'
    )
if config_data["log_level"] == "ERROR":
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M',
        filename=config_data["log_file"],
        filemode='w'
    )

# prepare database connect
restWrapper = couch_backend.rest.RestWrapper()
restWrapper.setHost( config_data["couch_host"] )
restWrapper.setPort( config_data["couch_port"] )
restWrapper.setPassword( config_data["couch_passwd"] )
restWrapper.setUser( config_data["couch_user"] )
restWrapper.setDB( config_data["couch_db"] )

# check database
response = restWrapper.getAllDBs()
logging.debug( "Founded data bases: ")
logging.debug( response.text )
if config_data["couch_db"] in json.loads(response.text):
    logging.debug("I found database " + config_data["couch_db"])
else:
    logging.info( "I can not found database " + config_data["couch_db"] + " and create now!")
    response = restWrapper.createDB( config_data["couch_db"] )
    logging.info( response.text )


# check password protection
response = restWrapper.getDocValue( "auth_key" )
print( response.text )
auth_key_data = json.loads(response.text, 'utf8')
if "error" in auth_key_data:
    if auth_key_data["error"] == "not_found":
        logging.info( "Can not found document auth_key and create with default password" )
        json_code = '{ \n'
        json_code += '"document_type": "app_config", \n'
        json_code += '"passwd_hash": "613367845fd07938881688f6c7e222497d778db3c3d7ff85c764498347d495c9", \n'
        json_code += '"salt": "tuxerjoch" \n'
        json_code += '}'

        response = restWrapper.insertNamedDoc( "auth_key", json_code )
        logging.info( response.text )
    else:
        logging.error( "Unknown error: " )
        logging.error( auth_key_data["error"] + ": " + auth_key_data["reason"] )


# init controller
home_page          = controls.home.Home( restWrapper )
controllNewArticle = controls.article.NewArticle( restWrapper )
controllAuth       = controls.auth.Auth( restWrapper )

# set routs
app.route('/', ['GET'], home_page.start_get)
app.route('/login', ['GET'], controllAuth.login_get)
app.route('/login', ['POST'], controllAuth.login_post)
app.route('/new_article', ['GET'], controllNewArticle.new_get)
app.route('/new_article', ['POST'], controllNewArticle.new_post)
app.route('/view_article/<name>', ['GET'], controllNewArticle.view_article_get)


bottle.run(app, host=config_data["webservice_host"], port=config_data["webservice_port"])
