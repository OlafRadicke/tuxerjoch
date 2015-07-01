import bottle
import json
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

# repairer database connect
restWrapper = couch_backend.rest.RestWrapper()
restWrapper.setHost( config_data["couch_host"] )
restWrapper.setPort( config_data["couch_port"] )
restWrapper.setPassword( config_data["couch_passwd"] )
restWrapper.setUser( config_data["couch_user"] )
restWrapper.setDB( config_data["couch_db"] )

# check database
response = restWrapper.getAllDBs()
print( response.text )
if config_data["couch_db"] in json.loads(response.text):
    print( "I found database " + config_data["couch_db"])
else:
    print( "I dont found database " + config_data["couch_db"] + " and create now!")
    response = restWrapper.createDB( config_data["couch_db"] )
    print( response.text )

# init controller
home_page = controls.home.Home( restWrapper )
controllNewArticle = controls.article.NewArticle( restWrapper )

# set routs
app.route('/', ['GET'], home_page.start_get)
app.route('/login', ['GET'], login)
app.route('/post_login', ['POST'], post_login)
app.route('/new_article', ['GET'], controllNewArticle.new_get)
app.route('/new_article', ['POST'], controllNewArticle.new_post)

bottle.run(app, host=config_data["webservice_host"], port=config_data["webservice_port"])
