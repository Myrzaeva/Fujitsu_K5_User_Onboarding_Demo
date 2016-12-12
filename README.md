# Fujitsu K5 Example User OnBoarding APIs
Platform: Fujitsu K5 IaaS
Project to hold my OpenStack K5 Python 2.7 API Scripts integrated with Flask 

This is an example python flask application used to illustrate how to automate the onboarding 
of new users to Fujitsu's K5 platform via its APIs.

It has the following functionality :

(i) Add new user to existing group and project

(ii) Add new user to new group and project

(iii) Add existing user to an existing project

(iv) Add existing user to new group and project


Installation
(Ubuntu 14.04 with Python 2.7)
- git clone https://github.com/allthingsclowd/Fujitsu_K5_User_Onboarding_Demo
- cd to the directory where requirements.txt is located.
- activate your virtualenv.
- run: pip install -r requirements.txt in your shell
- export PORT=5000
- cd app
- ./run.py
- navigate to http://localhost:5000/login

(Cloud Foundry)
- git clone https://github.com/allthingsclowd/Fujitsu_K5_User_Onboarding_Demo
- cd app
- cf push

Temporary URL where the demo app was active on K5 PaaS (you may be lucky!)
https://k5onboarding.uk-1.cf-app.net/

Next steps:
- Flask enhancements : migrate to flask-login, WTF forms
- Use tokens everywhere
