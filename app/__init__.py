from gconnect import GoolgleLogin
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, url_for, render_template, request, session

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['WTF_CSRF_CHECK_DEFAULT'] = False
csrf = CSRFProtect(app)

from api import api
from catalog import catalog
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(catalog, url_prefix='/catalog')


@app.before_request
def check_csrf():
    # print request.view_args
    # print session
    if request.endpoint in ['gconnect', 'test']:
        print 'ok'
        csrf.protect()


@app.route('/')
def index():
    return redirect(url_for('catalog.recentItems'))


@app.route('/gconnect', methods=['POST'])
def gconnect():
    code = request.data
    auth = GoolgleLogin()
    response = auth.Connect(code)
    output = 'OKOK'
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    if not access_token:
        response = make_response(json.dumps('Currentuser not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'\
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
