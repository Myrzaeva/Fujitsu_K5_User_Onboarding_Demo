#!/usr/bin/python
"""Summary
"""

from k5contractsettingsV1 import *
import requests, datetime, string, os.path, sys, time
from random import sample, choice


def get_globally_scoped_token():
    """Get a global project scoped auth token

    Returns:
        STRING: Globally Scoped Project  Token
    """
    identityURL = 'https://identity.gls.cloud.global.fujitsu.com/v3/auth/tokens'
    response = requests.post(identityURL,
                             headers={'Content-Type': 'application/json','Accept':'application/json'},
                             json={"auth":
                                    {"identity":
                                      {"methods":["password"],"password":
                                        {"user":
                                          {"domain":
                                            {"name":contract},
                                             "name":adminUser,
                                             "password": adminPassword
                                      }}},
                                      "scope":
                                        { "project":
                                          {"id":defaultid
                                  }}}})
    return response.headers['X-Subject-Token']


def get_scoped_token():
    """Get a regional project scoped auth token

    Returns:
        STRING: Regionally Scoped Project  Token
    """
    identityURL = 'https://identity.' + region + '.cloud.global.fujitsu.com/v3/auth/tokens'
    response = requests.post(identityURL,
                             headers={'Content-Type': 'application/json','Accept':'application/json'},
                             json={"auth":
                               {"identity":
                                 {"methods":["password"],"password":
                                   {"user":
                                     {"domain":
                                       {"name":contract},
                                        "name":adminUser,
                                        "password": adminPassword
                                }}},
                                "scope":
                                  { "project":
                                    {"id":projectid
                            }}}})

    return response.headers['X-Subject-Token']


def get_unscoped_token():
    """Get a regional unscoped auth token

    Returns:
        TYPE: Regional UnScoped Token
    """
    identityURL = 'https://identity.' + region + '.cloud.global.fujitsu.com/v3/auth/tokens'
    response = requests.post(identityURL,
                            headers={'Content-Type': 'application/json','Accept':'application/json'},
                            json={"auth":
                              {"identity":
                                {"methods":["password"],"password":
                                  {"user":
                                    {"domain":
                                      {"name":contract},
                                       "name":adminUser,
                                       "password": adminPassword
                            }}}}})

    return response.headers['X-Subject-Token']

def get_unscoped_idtoken():
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
                                     {"contract_number":contract,
                                      "name":adminUser,
                                      "password": adminPassword
                            }}}}})

    return response.headers['X-Access-Token']


def assign_user_to_group(username,groupname):
    """Summary

    Args:
        username (TYPE): Description
        groupname (TYPE): Description

    Returns:
        TYPE: Description
    """
    # if user exists return its id otherwise return 'None'
    userid = get_itemid(get_keystoneobject_list('users'),username,'users')
    # if group exists return its id otherwise return 'None'
    groupid = get_itemid(get_keystoneobject_list('groups'),groupname,'groups')
   # modified this to be verified
    # the global rather than regional api is required to assign users to groups
    region = 'gls'
    # get a global domain scoped token
    unscoped_global_k5token = get_globally_scoped_token()
    identityURL = 'https://identity.' + region + '.cloud.global.fujitsu.com/v3/groups/' + groupid + '/users/' + userid
    # make the put rest request
    response = requests.put(identityURL, headers={'X-Auth-Token':unscoped_global_k5token,'Content-Type': 'application/json'})
    return response

def assign_role_to_group_on_domain(group,role):
    """Summary

    Args:
        group (TYPE): Description
        role (TYPE): Description

    Returns:
        TYPE: Description
    """
    # if group exists return its id otherwisw return 'None'
    groupid = get_itemid(get_keystoneobject_list('groups'),group,'groups')
    # if role exists return its id otherwise return 'None'
    roleid = get_itemid(get_keystoneobject_list('roles'),role,'roles')
    # get a regional domain scoped token to make queries to facilitate conversion of object names to ids
    unscoped_k5token = get_unscoped_token()
    # the regional rather than global api is required for this call
    identityURL = 'https://identity.' + region + '.cloud.global.fujitsu.com/v3/domains/' + contractid + '/groups/' + groupid + '/roles/' + roleid
    # make the put rest api request
    response = requests.put(identityURL, headers={'X-Auth-Token':unscoped_k5token,'Content-Type': 'application/json','Accept':'application/json'})

    return response

def assign_role_to_user_and_project(username,project,role):
    """Summary

    Args:
        username (TYPE): Description
        project (TYPE): Description
        role (TYPE): Description

    Returns:
        TYPE: Description
    """
    # if user exists return its id otherwise return 'None'
    userid = get_itemid(get_keystoneobject_list('users'),username,'users')
    # if project exists return its id otherwise return 'None'
    projectid = get_itemid(get_keystoneobject_list('projects'),project,'projects')
    # if role exists return its id otherwise return 'None'
    roleid = get_itemid(get_keystoneobject_list('roles'),role,'roles')
    # get a regional domain scoped token to make queries to facilitate conversion of object names to ids
    k5token = get_unscoped_token()

    identityURL = 'https://identity.' + region + '.cloud.global.fujitsu.com/v3/projects/' + projectid + '/users/' + userid + '/roles/' + roleid
    response = requests.put(identityURL,
                            headers={'X-Auth-Token':k5token,'Content-Type': 'application/json','Accept':'application/json'})

    return response

def assign_role_to_group_and_project(group,project,role):
    """Summary

    Args:
        group (TYPE): Description
        project (TYPE): Description
        role (TYPE): Description

    Returns:
        TYPE: Description
    """
    # if group exists return its id otherwise return 'None'
    groupid = get_itemid(get_keystoneobject_list('groups'),group,'groups')
    # if project exists return its id otherwise return 'None'
    projectid = get_itemid(get_keystoneobject_list('projects'),project,'projects')
    # if role exists return its id otherwise return 'None'
    roleid = get_itemid(get_keystoneobject_list('roles'),role,'roles')
    # get a regional domain scoped token to make queries to facilitate conversion of object names to ids
    k5token = get_unscoped_token()

    identityURL = 'https://identity.' + region + '.cloud.global.fujitsu.com/v3/projects/' + projectid + '/groups/' + groupid + '/roles/' + roleid
    response = requests.put(identityURL,
                            headers={'X-Auth-Token':k5token,'Content-Type': 'application/json','Accept':'application/json'})

    return response

def create_new_project(project):
    """Summary

    Args:
        project (TYPE): Description

    Returns:
        TYPE: Description
    """
    # get a regional domain scoped token to make queries to facilitate conversion of object names to ids
    unscoped_k5token = get_unscoped_token()
    identityURL = 'https://identity.' + region + '.cloud.global.fujitsu.com/v3/projects?domain_id=' + contractid
    response = requests.post(identityURL,
                             headers={'X-Auth-Token':unscoped_k5token,'Content-Type': 'application/json','Accept':'application/json'},
                             json={"project":
                               {"description": "Programatically created project",
                                "domain_id": contractid,
                                "enabled": True,
                                "is_domain": False,
                                "name": project
                            }})

    #print response.json() 201 success 409 duplicate
    return response

def create_new_group(project):
    """Summary

    Args:
        project (TYPE): Description

    Returns:
        TYPE: Description
    """
    k5token = get_globally_scoped_token()
    groupname = project + '_Admin'
    groupURL = 'https://identity.gls.cloud.global.fujitsu.com/v3/groups'
    response = requests.post(groupURL,
                             headers={'X-Auth-Token':k5token,'Content-Type': 'application/json'},
                             json={"group":
                                    {"description": "auto-generated project",
                                     "domain_id": contractid,
                                     "name": groupname
                                  }})
    groupDetail = response.json()
    return groupDetail['group']['name']

# Gets generic keystone list of projects,users,roles or groups depending on the object type passed in to the call
def get_keystoneobject_list(objecttype):
    """Summary

    Args:
        objecttype (TYPE): Description

    Returns:
        TYPE: Description
    """
    # get a regional domain scoped token to list the objects
    k5token = get_unscoped_token()

    identityURL = 'https://identity.' + region + '.cloud.global.fujitsu.com/v3/' + objecttype + '?domain_id=' + contractid
    response = requests.get(identityURL,
                            headers={'X-Auth-Token':k5token,'Content-Type': 'application/json','Accept':'application/json'})

    return response.json()

# get id from name in a list
def get_itemid(itemlist,itemname,itemtype):
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


def add_new_user(userDetails):
    """Summary

    Args:
        userDetails (TYPE): Description

    Returns:
        TYPE: Description
    """
    global_auth_k5token = get_unscoped_idtoken()
    centralIdUrl = 'https://k5-apiportal.paas.cloud.global.fujitsu.com/API/v1/api/users'

    response = requests.post(centralIdUrl,
                             headers={'Token':global_auth_k5token,'Content-Type': 'application/json'},
                             json={"user_last_name":userDetails[1],
                                   "user_first_name":userDetails[0],
                                   "login_id":userDetails[2],
                                   "user_description":"Automated Account Setup",
                                   "mailaddress":userDetails[3],
                                   "user_status":"1",
                                   "password":userDetails[4],
                                   "language_code":"en",
                                   "role_code":"01"
                            })
    return response

def main():
    """Summary

    Returns:
        TYPE: Description
    """
    print "K5 Wrapper Module"

if __name__ == "__main__":
    main()
