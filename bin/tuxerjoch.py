import bottle
import json
import logging

import controls.article
import controls.home
import couch_backend.rest

app = bottle.Bottle()

#@app.get('/login') # or @route('/login')
def login():
    return '''
        <form action="/post_login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''

#@app.post('/login') # or @route('/login', method='POST')
def post_login():
    username = bottle.request.forms.get('username')
    password = bottle.request.forms.get('password')
    if check_login(username, password):
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"

# Reade config file
with open("tuxerjoch.conf") as json_file:
    config_data = json.load(json_file)

# prepare logger
if config_data["log_level"] == "DEBUG":
    logging.basicConfig(filename=config_data["log_file"],level=logging.DEBUG)
if config_data["log_level"] == "ERROR":
    logging.basicConfig(filename=config_data["log_file"],level=logging.ERROR)

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
    logging.debug( "I dont found database " + config_data["couch_db"] + " and create now!")
    response = restWrapper.createDB( config_data["couch_db"] )
    logging.debug( response.text )

# init controller
home_page = controls.home.Home( restWrapper )
controllNewArticle = controls.article.NewArticle( restWrapper )

# set routs
app.route('/', ['GET'], home_page.start_get)
app.route('/login', ['GET'], login)
app.route('/new_article', ['GET'], controllNewArticle.new_get)
app.route('/new_article', ['POST'], controllNewArticle.new_post)
app.route('/post_login', ['POST'], post_login)
app.route('/view_article/<name>', ['GET'], controllNewArticle.view_article_get)


bottle.run(app, host=config_data["webservice_host"], port=config_data["webservice_port"])
