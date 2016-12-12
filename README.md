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


#Installation

#Ubuntu 14.04 with Python 2.7
- git clone https://github.com/allthingsclowd/Fujitsu_K5_User_Onboarding_Demo
- cd to the directory where requirements.txt is located.
- activate your virtualenv.
- run: pip install -r requirements.txt in your shell
- export PORT=5000
- cd app
- ./run.py
- navigate to http://localhost:5000/login

#Cloud Foundry
- git clone https://github.com/allthingsclowd/Fujitsu_K5_User_Onboarding_Demo
- cd app
- cf push

#Instructions
1. Login using your K5 credentials - You MUST be a Contract Admin to login, non admins will simply be returned to the login screen.
2. Enter the email address of the user to be added - email address must be of the format firstname.lastname@company.com. If the user does not exist they will be added to the default project first as a _member_ role before being added to the project as a cpf_systemowner. If the user already exists they will simply be added to the project identified next.
3. Enter the project that the user is to be added to - if the project already exists the user will be added to this project. If the project does not exist then it will first be created, along with a group named [projectName]_Admin with the cpf_systemowner role and then the user will be assigned to this group.
4. Select the Adduser button - wait - after about 90 seconds you should get a results screen with the new username and password - ensure to copy this as it's not recorded anywhere.
Temporary URL where a demo of this app was active on K5 Cloud Foundry PaaS when this blog was originally published (you may be lucky!)
https://k5onboarding.uk-1.cf-app.net/

#Next steps (feel free to contribute, not just suggestions but code too) :
- Flask enhancements : migrate to flask-login, WTF forms
- Use tokens everywhere
- Add Flask user updates
- Email results directly to new user with welcome pack
