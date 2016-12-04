from flask import render_template, session, request, redirect, url_for
from app import app
import os
import AddUserToProjectv2 as K5User
import k5APIwrappersV1 as K5API
from functools import wraps

app.secret_key = os.urandom(24)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['token'] is None:
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET','POST'])
def index():
   session['token'] = None
   if request.method == 'POST':

     adminUser =  request.form.get('k5username',None)
     adminPassword = request.form.get('k5password',None)
     contract = request.form.get('k5contract',None)
     region = request.form.get('k5region',None)
     print region
     result = K5API.get_unscoped_token(adminUser,adminPassword,contract,region)
     print result
     if result != 'Authorisation Failure':
       session['token'] = result
       return redirect(url_for('adduser'))
     else:
       return render_template('hello-flask-login.html',
                           title='K5 Admin Portal (Beta)')
   else:
     return render_template('hello-flask-login.html',
                           title='K5 Admin Portal (Beta)')


@app.route('/adduser',methods=['GET','POST'])
@login_required
def adduser():
  if request.method == 'POST':
    if request.form.get('AddUser', None) == "Add User":
      #####
      ##### STOPPED HERE
      #######
      ####### In the process of tokenising all the functions to avoid
      ########## passing username and password
      return redirect(url_for('userstatus'))
    else:
      if request.form.get('Logout', None) == "Logout":
        return redirect(url_for('logout'))

  if request.method == 'GET':
    return render_template('hello-flask-adduser.html',
                           title='K5 Add User')

@app.route('/userstatus',methods=['GET','POST'])
@login_required
def userstatus():
  if request.method == 'POST':
    if request.form.get('AddUser', None) == "Add Another User":
      return redirect(url_for('adduser'))
    else:
      if request.form.get('Logout', None) == "Logout":
        return redirect(url_for('logout'))

  if request.method == 'GET':
    return render_template('hello-flask-result.html',
                           title='K5 New User Details',
                           userstatus = 'Put Results From New User Here!')

@app.route('/logout')
@login_required
def logout():
   # remove the username from the session if it is there
  session.pop('token', None)
  return redirect(url_for('index'))
