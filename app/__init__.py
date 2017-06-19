import json
from gconnect import GoolgleLogin
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask import Flask, redirect, url_for, render_template, request, session,\
    make_response, jsonify, flash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['WTF_CSRF_CHECK_DEFAULT'] = False
csrf = CSRFProtect(app)

from api import api
from catalog import catalog
from models import Category, Item, User

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(catalog, url_prefix='/catalog')


@app.before_request
def check_csrf():
    if request.endpoint in ['gconnect', 'gdisconnect']:
        csrf.protect()


@app.errorhandler(CSRFError)
def csrf_error(reason):
    response = make_response(json.dumps(reason.description), 401)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/')
def index():
    return redirect(url_for('catalog.recentItems'))


@app.route('/gconnect', methods=['POST'])
def gconnect():
    glogin = GoolgleLogin()
    google_resp = glogin.Connect(request.data)
    if google_resp[1] != 200:
        response = make_response(json.dumps(google_resp[0]), google_resp[1])
        response.headers['Content-Type'] = 'application/json'
        return response

    userinfo = glogin.GetInfo()

    user_id = getUserID(userinfo['email'])
    if not user_id:
        user_id = createUser(userinfo)

    session['user_id'] = user_id
    session['username'] = userinfo['name']
    session['picture'] = userinfo['picture']
    session['email'] = userinfo['email']
    session['access_token'] = glogin.credentials.access_token
    flash(
        'You have signed in successfully, welcome %s' % session['username'],
        'info')
    return jsonify(
        msg='Connected to : ',
        username=session['username'],
        picture=session['picture'])


@app.route('/gdisconnect', methods=['POST'])
def gdisconnect():
    glogin = GoolgleLogin()
    glogin.Disconnect(session.get('access_token'))
    del session['user_id']
    del session['username']
    del session['picture']
    del session['email']
    del session['access_token']
    flash('You have signed out', 'info')
    return redirect(url_for('index'))


def createUser(userinfo):
    newUser = User(name=userinfo['name'],
                   email=userinfo['email'],
                   picture=userinfo['picture'])
    db.session.add(newUser)
    db.session.commit()
    user = db.session.query(User).filter_by(email=userinfo['email']).first()
    return user.id


def getUserInfo(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    return user


def getUserID(email):
    try:
        user = db.session.query(User).filter_by(email=email).first()
        return user.id
    except AttributeError:
        return None
