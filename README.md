# Fujitsu K5 Example User On Boarding APIs
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
- git clone <this repo>
- cd to the directory where requirements.txt is located.
- activate your virtualenv.
- run: pip install -r requirements.txt in your shell
- export PORT=5000
- cd app
- ./run.py
- navigate to http://localhost:5000/login

(Cloud Foundry)
- git clone <this repo>
- cd app
- cf push
