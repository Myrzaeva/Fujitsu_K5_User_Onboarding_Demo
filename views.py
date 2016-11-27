from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'landg'}  # fake user
    return render_template('hello-flask-login.html',
                           title='K5 Admin Portal (Beta)',
                           user=user)

@app.route('/adduser')
def adduser():
    user = {'username': 'landg'}  # fake user
    return render_template('hello-flask-adduser.html',
                           title='K5 Add User',
                           user=user)

@app.route('/userstatus')
def userstatus():
    user = {'username': 'landg'}  # fake user
    return render_template('hello-flask-result.html',
                           title='K5 User Status',
                           user=user)
