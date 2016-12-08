#!/usr/bin/python
"""Summary
"""

#from k5contractsettingsV1 import *
import requests
import datetime
import string
import os.path
import sys
import time
from random import sample, choice


def get_globally_scoped_token(adminUser, adminPassword, contract, defaultid, region):
    """Get a global project scoped auth token

    Returns:
        STRING: Globally Scoped Project  Token
    """
    identityURL = 'https://identity.gls.cloud.global.fujitsu.com/v3/auth/tokens'
    response = requests.post(identityURL,
                             headers={'Content-Type': 'application/json',
                                      'Accept': 'application/json'},
                             json={"auth":
                                   {"identity":
                                    {"methods": ["password"], "password":
                                     {"user":
                                        {"domain":
                                         {"name": contract},
                                         "name": adminUser,
                                         "password": adminPassword
                                         }}},
                                    "scope":
                                    {"project":
                                     {"id": defaultid
                                      }}}})
    return response
#    return response.headers['X-Subject-Token']


def get_globally_rescoped_token(globaltoken, defaultid):
    """Get a global project scoped auth token

    Returns:
        STRING: Globally Scoped Project  Token
    """
    identityURL = 'https://identity.gls.cloud.global.fujitsu.com/v3/auth/tokens'
    response = requests.post(identityURL,
                             headers={'Content-Type': 'application/json',
                                      'Accept': 'application/json'},
                             json={
                                 "auth": {
                                     "identity": {
                                         "methods": [
                                             "token"
                                         ],
                                         "token": {
                                             "id": globaltoken
                                         }
                                     },
                                     "scope": {
                                         "project": {
                                             "id": defaultid
                                         }
                                     }
                                 }
                             })
    return response
#    return response.headers['X-Subject-Token']


def get_re_unscoped_token(k5token, region):
    """Get a regional project scoped auth token
    Returns:
        STRING: Regionally Scoped Project  Token
    """
    print k5token
    print region
    identityURL = 'https://identity.' + region + \
        '.cloud.global.fujitsu.com/v3/auth/tokens'
    print identityURL
    tokenbody = {
        "auth": {
            "identity": {
                "methods": [
                    "token"
                ],
                "token": {
                    "id": k5token
                }
            },
        }
    }
    print tokenbody
    response = requests.post(identityURL,
                             headers={'Content-Type': 'application/json',
                                      'Accept': 'application/json'},
                             json=tokenbody)

    if response.status_code == 201:
        # return response.headers['X-Subject-Token']
        print response.headers['X-Subject-Token']
        return response
    else:
        print "Rescope Failure"
        print response
        print response.headers
        return 'Re-authentication Failure'


def get_rescoped_token(k5token, projectid, region):
    """Get a regional project scoped auth token
    Returns:
        STRING: Regionally Scoped Project  Token
    """
    identityURL = 'https://identity.' + region + \
        '.cloud.global.fujitsu.com/v3/auth/tokens'
    response = requests.post(identityURL,
                             headers={'Content-Type': 'application/json',
                                      'Accept': 'application/json'},
                             json={
                                 "auth": {
                                     "identity": {
                                         "methods": [
                                             "token"
                                         ],
                                         "token": {
                                             "id": k5token
                                         }
                                     },
                                     "scope": {
                                         "project": {
                                             "id": projectid
                                         }
                                     }
                                 }
                             })

    if response.status_code == 201:
        # return response.headers['X-Subject-Token']
        return response
    else:
        return 'Re-authentication Failure'


def get_scoped_token(adminUser, adminPassword, contract, projectid, region):
    """Get a regional project scoped auth token
    Returns:
        STRING: Regionally Scoped Project  Token
    """
    identityURL = 'https://identity.' + region + \
        '.cloud.global.fujitsu.com/v3/auth/tokens'
    response = requests.post(identityURL,
                             headers={'Content-Type': 'application/json',
                                      'Accept': 'application/json'},
                             json={"auth":
                                   {"identity":
                                    {"methods": ["password"], "password":
                                     {"user":
                                      {"domain":
                                       {"name": contract},
                                       "name": adminUser,
                                       "password": adminPassword
                                       }}},
                                       "scope":
                                       {"project":
                                        {"id": projectid
                                         }}}})

    return response.headers['X-Subject-Token']


def get_unscoped_token(adminUser, adminPassword, contract, region):
    """Get a regional unscoped auth token

    Returns:
        TYPE: Regional UnScoped Token
    """
    identityURL = 'https://identity.' + region + \
        '.cloud.global.fujitsu.com/v3/auth/tokens'
    response = requests.post(identityURL,
                             headers={'Content-Type': 'application/json',
                                      'Accept': 'application/json'},
                             json={"auth":
                                   {"identity":
                                    {"methods": ["password"], "password":
                                     {"user":
                                        {"domain":
                                         {"name": contract},
                                            "name": adminUser,
                                            "password": adminPassword
                                         }}}}})

    if response.status_code == 201:
        # return response.headers['X-Subject-Token']
        return response
    else:
        return 'Authentication Failure'


def get_unscoped_idtoken(adminUser, adminPassword, contract):
    """Summary - get a central identity portal token may be same as global token???

    Returns:
        TYPE: Description
    """
    response = requests.post('https://auth-api.jp-east-1.paas.cloud.global.fujitsu.com/API/paas/auth/token',
                             headers={'Content-Type': 'application/json'},
                             json={"auth":
                                   {"identity":
                                    {"password":
                                     {"user":
                                      {"contract_number": contract,
                                       "name": adminUser,
                                       "password": adminPassword
                                       }}}}})

    return response.headers['X-Access-Token']


def assign_user_to_group(global_token, regional_token, contractid, region, username, groupname):
    """Summary

    Args:
        username (TYPE): Description
        groupname (TYPE): Description

    Returns:
        TYPE: Description
    """
    # if user exists return its id otherwise return 'None'
    userid = get_itemid(get_keystoneobject_list(
        regional_token, region, contractid, 'users'), username, 'users')
    # if group exists return its id otherwise return 'None'
    groupid = get_itemid(get_keystoneobject_list(
        regional_token, region, contractid, 'groups'), groupname, 'groups')
   # modified this to be verified
    # the global rather than regional api is required to assign users to groups
    region = 'gls'
    # get a global domain scoped token
    #unscoped_global_k5token = get_globally_scoped_token()
    identityURL = 'https://identity.' + region + \
        '.cloud.global.fujitsu.com/v3/groups/' + groupid + '/users/' + userid
    # make the put rest request
    response = requests.put(identityURL, headers={
                            'X-Auth-Token': global_token, 'Content-Type': 'application/json'})
    return response


def assign_role_to_group_on_domain(k5token, contractid, region, group, role):
    """Summary

    Args:
        group (TYPE): Description
        role (TYPE): Description

    Returns:
        TYPE: Description
    """
    # if group exists return its id otherwisw return 'None'
    groupid = get_itemid(get_keystoneobject_list(
        k5token, region, contractid, 'groups'), group, 'groups')
    # if role exists return its id otherwise return 'None'
    roleid = get_itemid(get_keystoneobject_list(
        k5token, region, contractid, 'roles'), role, 'roles')
    # get a regional domain scoped token to make queries to facilitate conversion of object names to ids
    #unscoped_k5token = get_unscoped_token()
    # the regional rather than global api is required for this call
    identityURL = 'https://identity.' + region + '.cloud.global.fujitsu.com/v3/domains/' + \
        contractid + '/groups/' + groupid + '/roles/' + roleid
    # make the put rest api request
    response = requests.put(identityURL, headers={
                            'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})

    return response


def assign_role_to_user_and_project(k5token, contractid, region, username, project, role):
    """Summary

    Args:
        username (TYPE): Description
        project (TYPE): Description
        role (TYPE): Description

    Returns:
        TYPE: Description
    """
    # if user exists return its id otherwise return 'None'
    userid = get_itemid(get_keystoneobject_list(
        k5token, region, contractid, 'users'), username, 'users')
    # if project exists return its id otherwise return 'None'
    projectid = get_itemid(get_keystoneobject_list(
        k5token, region, contractid, 'projects'), project, 'projects')
    # if role exists return its id otherwise return 'None'
    roleid = get_itemid(get_keystoneobject_list(
        k5token, region, contractid, 'roles'), role, 'roles')
    # get a regional domain scoped token to make queries to facilitate conversion of object names to ids
    #k5token = get_unscoped_token()

    identityURL = 'https://identity.' + region + '.cloud.global.fujitsu.com/v3/projects/' + \
        projectid + '/users/' + userid + '/roles/' + roleid
    response = requests.put(identityURL,
                            headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})

    return response


def assign_role_to_group_and_project(k5token, contractid, region, group, project, role):
    """Summary

    Args:
        group (TYPE): Description
        project (TYPE): Description
        role (TYPE): Description

    Returns:
        TYPE: Description
    """
    # if group exists return its id otherwise return 'None'
    groupid = get_itemid(get_keystoneobject_list(
        k5token, region, contractid, 'groups'), group, 'groups')
    # if project exists return its id otherwise return 'None'
    projectid = get_itemid(get_keystoneobject_list(
        k5token, region, contractid, 'projects'), project, 'projects')
    # if role exists return its id otherwise return 'None'
    roleid = get_itemid(get_keystoneobject_list(
        k5token, region, contractid, 'roles'), role, 'roles')
    # get a regional domain scoped token to make queries to facilitate conversion of object names to ids
    #k5token = get_unscoped_token()

    identityURL = 'https://identity.' + region + '.cloud.global.fujitsu.com/v3/projects/' + \
        projectid + '/groups/' + groupid + '/roles/' + roleid
    response = requests.put(identityURL,
                            headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})

    return response


def create_new_project(k5token, contractid, region, project):
    """Summary

    Args:
        project (TYPE): Description

    Returns:
        TYPE: Description
    """
    # get a regional domain scoped token to make queries to facilitate conversion of object names to ids
    #unscoped_k5token = get_unscoped_token(adminUser,adminPassword,contract,region)
    identityURL = 'https://identity.' + region + \
        '.cloud.global.fujitsu.com/v3/projects?domain_id=' + contractid
    response = requests.post(identityURL,
                             headers={
                                 'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                             json={"project":
                                   {"description": "Programatically created project",
                                    "domain_id": contractid,
                                    "enabled": True,
                                    "is_domain": False,
                                    "name": project
                                    }})

    # print response.json() 201 success 409 duplicate
    return response


def create_new_group(global_k5token, contractid, region, project):
    """Summary

    Args:
        project (TYPE): Description

    Returns:
        TYPE: Description
    """
    #k5token = get_globally_scoped_token(adminUser,adminPassword,contract,region)
    groupname = project + '_Admin'

    groupURL = 'https://identity.gls.cloud.global.fujitsu.com/v3/groups'
    response = requests.post(groupURL,
                             headers={'X-Auth-Token': global_k5token,
                                      'Content-Type': 'application/json'},
                             json={"group":
                                   {"description": "auto-generated project",
                                    "domain_id": contractid,
                                    "name": groupname
                                    }})
    groupDetail = response.json()

    return groupDetail['group']['name']

# Gets generic keystone list of projects,users,roles or groups depending
# on the object type passed in to the call


def get_keystoneobject_list(k5token, region, contractid, objecttype):
    """Summary

    Args:
        objecttype (TYPE): Description

    Returns:
        TYPE: Description
    """
    # get a regional domain scoped token to list the objects
    #k5token = get_unscoped_token(adminUser,adminPassword,contract,region)

    identityURL = 'https://identity.' + region + \
        '.cloud.global.fujitsu.com/v3/' + objecttype + '?domain_id=' + contractid
    response = requests.get(identityURL,
                            headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})

    return response.json()

# get id from name in a list


def get_itemid(itemlist, itemname, itemtype):
    """Summary

    Args:
        itemlist (TYPE): Description
        itemname (TYPE): Description
        itemtype (TYPE): Description

    Returns:
        TYPE: Description
    """
    itemid = 'None'

    for item in itemlist[itemtype]:
        if (item.get('name') == itemname):
            itemid = item.get('id')
            break
    return itemid


def add_new_user(idtoken, contract, region, userDetails):
    """Summary

    Args:
        userDetails (TYPE): Description

    Returns:
        TYPE: Description
    """
    #global_auth_k5token = get_unscoped_idtoken(adminUser,adminPassword,contract,region)
    centralIdUrl = 'https://k5-apiportal.paas.cloud.global.fujitsu.com/API/v1/api/users'

    response = requests.post(centralIdUrl,
                             headers={'Token': idtoken,
                                      'Content-Type': 'application/json'},
                             json={"user_last_name": userDetails[1],
                                   "user_first_name": userDetails[0],
                                   "login_id": userDetails[2],
                                   "user_description": "Automated Account Setup",
                                   "mailaddress": userDetails[3],
                                   "user_status": "1",
                                   "password": userDetails[4],
                                   "language_code": "en",
                                   "role_code": "01"
                                   })
    return response


def main():
    """Summary

    Returns:
        TYPE: Description
    """
    print "K5 Wrapper Module"
    adminUser = 'landg'
    adminPassword = 'happybirthdaytome16'
    contract = 'YssmW1yI'
    region = 'uk-1'
    defaultid = 'eadb882573ac40b1b101eac93009a313'

    k5unscopedtoken = get_unscoped_token(
        adminUser, adminPassword, contract, region)
    print "Unscoped token - " + str(k5unscopedtoken.headers['X-Subject-Token'])
    # for role in k5unscopedtoken.json()['token']['roles']:
    # if role['name'] == 'cpf_admin':
    # print "I'm an Administrator"
    # elif role['name'] == 'cpf_systemowner':
    #  print "I'm a Domain Owner"
    # else:
    # print "I'm not worthy!!!"

    # print "\nRoles - " + str(k5unscopedtoken.json()['token']['roles'])
    # print "\nDefault Project Id - " + str(k5unscopedtoken.json()['token']['project'].get('id'))
    # print "\nDefault Contract Id - " + str(k5unscopedtoken.json()['token']['project']['domain'].get('id'))
    #k5rescopedtoken = get_rescoped_token(k5unscopedtoken.headers['X-Subject-Token'],'eadb882573ac40b1b101eac93009a313','uk-1')
    # print "Rescoped Project Token - " +
    # str(k5rescopedtoken.headers['X-Subject-Token'])

    k5unscopedtoken2 = get_re_unscoped_token(
        k5unscopedtoken.headers['X-Subject-Token'], 'uk-1')
    oldunscopedtoken = k5unscopedtoken2.headers['X-Subject-Token']
    print "\n New Token " + oldunscopedtoken

    k5unscopedtoken3 = get_re_unscoped_token(oldunscopedtoken, 'uk-1')
    oldunscopedtoken2 = k5unscopedtoken3.headers['X-Subject-Token']
    print "\n New Token 2 " + oldunscopedtoken2

    #k5unscopedtoken4 = get_re_unscoped_token('1221534406584fd585371cdd218a7ae5','uk-1')
    #oldunscopedtoken3 = k5unscopedtoken4.headers['X-Subject-Token']
   # print  "\n New Token 2 " + oldunscopedtoken3
    # for i in range(9):
    #  print "\n\n New Unscoped Regional Token"
    # newtoken = get_re_unscoped_token(oldunscopedtoken,'uk-1')
    # print newtoken.headers['X-Subject-Token']
    #oldtoken = newtoken.headers['X-Subject-Token']

    # print "Re - Unscoped Token - " + str(k5unscopedtoken2.headers['X-Subject-Token'])
    # print k5unscopedtoken2.json()
   # print "\n\n"
    #globaltoken = get_globally_scoped_token(adminUser,adminPassword,contract,defaultid,region)
    #oldtoken = globaltoken.headers['X-Subject-Token']
    # print globaltoken.headers['X-Subject-Token']
    # for i in range(9):
    # print "\n\n New Token"
    #newtoken = get_globally_rescoped_token(oldtoken,defaultid)
    # print newtoken.headers['X-Subject-Token']
    #oldtoken = newtoken.headers['X-Subject-Token']


if __name__ == "__main__":
    main()
