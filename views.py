from flask import render_template, session, request, redirect, url_for
from app import app
import os

app.secret_key = os.urandom(24)

@app.route('/login', methods=['GET','POST'])
def index():
   if request.method == 'POST':
     session.pop('user',None)


     session['user'] =  request.form['k5username']
     session['password'] = request.form['k5password']
     session['contract'] = request.form['k5contract']
     session['region'] = request.form['k5region']

     if session['password']  == 'password':
       return redirect(url_for('adduser'))
     else:
       return render_template('hello-flask-login.html',
                           title='K5 Admin Portal (Beta)')

   else:
     return render_template('hello-flask-login.html',
                           title='K5 Admin Portal (Beta)')


@app.route('/adduser')
def adduser():
    return render_template('hello-flask-adduser.html',
                           title='K5 Add User')

@app.route('/userstatus')
def userstatus():
    return render_template('hello-flask-result.html',
                           title='K5 User Status')
