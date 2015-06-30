#from bottle import Bottle, run
import bottle
import controls.article

app = bottle.Bottle()

@app.get('/')
def home():
    name = "Olaf"
    return bottle.template('home', name=name)


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


app.route('/login', ['GET'], login)
app.route('/post_login', ['POST'], post_login)
app.route('/new_article', ['GET'], controls.article.new_get)
app.route('/new_article', ['POST'], controls.article.new_post)

bottle.run(app, host='localhost', port=8080)
