from flask import render_template, session, request, redirect, url_for
from app import app
import os
import AddUserToProjectv3 as K5User
import k5APIwrappersV3 as K5API
from functools import wraps

app.secret_key = os.urandom(24)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['regionaltoken'] is None:
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def index():
    session['regionaltoken'] = None
    if request.method == 'POST':
        adminUser = request.form.get('k5username', None)
        adminPassword = request.form.get('k5password', None)
        contract = request.form.get('k5contract', None)
        region = request.form.get('k5region', None)
        regional_token = K5API.get_unscoped_token(
            adminUser, adminPassword, contract, region)
        defaultid = regional_token.json()['token']['project'].get('id')
        global_token = K5API.get_globally_scoped_token(
            adminUser, adminPassword, contract, defaultid, region)

        if regional_token != 'Authorisation Failure':
            for role in regional_token.json()['token']['roles']:
                if role['name'] == 'cpf_admin':

                    session['adminUser'] = adminUser
                    session['adminPassword'] = adminPassword
                    session['regionaltoken'] = regional_token.headers[
                        'X-Subject-Token']
                    session['globaltoken'] = global_token.headers[
                        'X-Subject-Token']
                    session['contract'] = contract
                    session['contractid'] = regional_token.json()['token']['project'][
                        'domain'].get('id')
                    session['defaultprjid'] = regional_token.json()['token'][
                        'project'].get('id')
                    session['region'] = region
                    return redirect(url_for('adduser'))
                else:
                    render_template('hello-flask-login.html',
                                    title='K5 Admin Portal (Beta)')
        else:
            return render_template('hello-flask-login.html',
                                   title='K5 Admin Portal (Beta)')
    else:
        return render_template('hello-flask-login.html',
                               title='K5 Admin Portal (Beta)')


@app.route('/adduser', methods=['GET', 'POST'])
@login_required
def adduser():
    if request.method == 'POST':
        if request.form.get('AddUser', None) == "Add User":
            adminUser = session['adminUser']
            adminPassword = session['adminPassword']
            contract = session['contract']
            contractid = session['contractid']
            region = session['region']
            defaultprjid = session['defaultprjid']
            regional_token = K5API.get_unscoped_token(
                adminUser, adminPassword, contract, region)
            global_token = K5API.get_globally_scoped_token(
                adminUser, adminPassword, contract, defaultprjid, region)
            id_token = K5API.get_unscoped_idtoken(
                adminUser, adminPassword, contract)

            newregionaltoken = regional_token.headers['X-Subject-Token']
            newglobaltoken = global_token.headers['X-Subject-Token']
            email = request.form.get('k5useremail', None)
            userProject = request.form.get('k5project', None)
            result = K5User.adduser_to_K5(id_token,
                                          newglobaltoken, newregionaltoken, contractid, contract, region, email, userProject)
            if result != None:
                session['newuserlogin'] = result[2]
                session['newuserpassword'] = result[4]

            return redirect(url_for('userstatus'))
        else:
            if request.form.get('Logout', None) == "Logout":
                return redirect(url_for('logout'))

    if request.method == 'GET':
        return render_template('hello-flask-adduser.html',
                               title='K5 Add User')


@app.route('/userstatus', methods=['GET', 'POST'])
@login_required
def userstatus():
    if request.method == 'POST':
        if request.form.get('AddUser', None) == "Add Another User":
            return redirect(url_for('adduser'))
        else:
            if request.form.get('Logout', None) == "Logout":
                return redirect(url_for('logout'))

    if request.method == 'GET':
        username = session['newuserlogin']
        userpassword = session['newuserpassword']
        return render_template('hello-flask-result.html',
                               title='K5 New User Details',
                               userstatus='Username : ' + username + ' | Password : ' + userpassword)


@app.route('/logout')
@login_required
def logout():
    # remove the username from the session if it is there
    session.pop('regionaltoken', None)
    session.pop('globaltoken', None)
    return redirect(url_for('index'))
