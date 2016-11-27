#!/usr/bin/python
"""Summary
"""
# Author : Graham Land
# Date:    08/11/2016
#
# Purpose: Add User to K5 and Project
#          If user already exists they will just be added to the project
#          If project already exists then user will just be added to the project
#          If both the user AND the project are new to the Domain EVERYTHING will be created
#          Warning - Don't lose the passwords - they are NOT written anywhere other then the console
#          Command line parameters -
#          -u user_email_address
#          -p project_name

#
# Prerequisites: k5contractsettings.py & k5APIwrappers.py files in the same directory
#                Ensure the k5contractsettings.py has a Domain/Contract Admin Account for the correct permissions
#
# adminUser = 'username'
# adminPassword = 'password'
# contract = 'contract_name'
# contractid = 'contract_id'
# defaultid = 'default_project_id'
# project = 'working_project'
# region = 'uk-1'
#
# blog:    https://allthingscloud.eu
# twitter: @allthingsclowd

from random import sample, choice
from k5APIwrappersV1 import *
import getopt

# generate random password
def get_password():
    """Summary

    Returns:
        TYPE: Description
    """
    chars = string.ascii_lowercase + string.digits
    length = 16
    return (''.join([choice(chars) for i in range(length)]))

def breakdown_user_from_email(useremail):
    """Summary

    Args:
        useremail (TYPE): Description

    Returns:
        TYPE: Description
    """
    firstnameEnd = useremail.find('.')
    surnameEnd = useremail.find('@')
    surname = useremail[firstnameEnd+1:surnameEnd]
    firstname = useremail[:firstnameEnd]
    username = (useremail[firstnameEnd+1:surnameEnd] + useremail[:1]).lower()
    password = get_password()
    return (firstname,surname,username,useremail,password)


def main():
    """Summary

    Returns:
        TYPE: Description
    """
    try:


        # ensure minimium commandline paramaters have been supplied
        if (len(sys.argv)<3):
            print("Usage1: %s -u 'user_email_address' -p 'project_name'" % sys.argv[0])
            sys.exit(2)

        # load the command line parameters
        myopts, args = getopt.getopt(sys.argv[1:],"u:p:",["user_email_address=","project_name="])
    except getopt.GetoptError:
        # if the parameters are incorrect display error message
        print("Usage2: %s -u 'user_email_address' -p 'project_name'" % sys.argv[0])
        sys.exit(2)

    #tester = [('graham.land@uk.fujitsu.com','iCloud18')   ]
    ###############################
    # o == option
    # a == argument passed to the o
    ###############################
    for o, a in myopts:
        if o in ('-u','--user_email_address'):
            email=a
        elif o in ('-p','--project_name'):
            userProject=a
        else:
            print("Usage3: %s -u 'user_email_address' -p 'project_name'" % sys.argv[0])

    UserStatusReport = {}
    userCounter = 0
    userDetails = breakdown_user_from_email(email)
    newuserid = get_itemid(get_keystoneobject_list('users'),userDetails[2],'users')

    # Check new user login is available, if not try adding '1' to it and testing again, repeat one more time for '2' before failing the user
    userStatus = False
    status = 'Step 1 - Initialise ...'
    UserStatusReport[email] = status,userDetails,userProject
    print status

    # if the username already exist warn and carry on
    if (newuserid != 'None'):
        userStatus = True
        status = 'Step 2 - User Login name already exists - Will add existing User to Project ...'
        userDetails = (userDetails[0],userDetails[1],userDetails[2],userDetails[3],"ExistingUserAddedToProject")
        UserStatusReport[email] = status,userDetails,userProject
        print status

    # if the user name does not exist add the new user
    else:
        userStatus = True

        # make rest api call to add new user
        result = add_new_user(userDetails)

        # if the result from the above call is successful
        if result.status_code == 200:
            userStatus = True
            status = 'Step 3 - User Added to Portal - continue ...'
            UserStatusReport[email] = status,userDetails,userProject
            print status

        # if the add new user api call failed report and exit
        else:
            userStatus = False
            status = 'Step 4 - Failed to Add User to Portal - Error, STOP!'
            UserStatusReport[email] = status,userDetails,userProject
            print status


        # Assign _member_ role to user in default project
        # if user has been added to authentication portal successfully
        if userStatus:

            # generate the default project name from the contract name
            defaultProject = contract + '-prj'

            defaultProjectid = get_itemid(get_keystoneobject_list('projects'),defaultProject,'projects')
            if (defaultProjectid != 'None'):
                result = assign_role_to_user_and_project(userDetails[2],defaultProject,'_member_')
                portal_sync_delay = 0

                # added a retry/delay routine here to allow sychronisation time between central portal and K5 IaaS regional portal
                while (portal_sync_delay < 4) and (result.status_code != 204):
                    time.sleep(5)
                    result = assign_role_to_user_and_project(userDetails[2],defaultProject,'_member_')
                    portal_sync_delay = portal_sync_delay + 1
                    status = 'Step 5 - User details not synced to IaaS portal - waiting 5 seconds before retrying up to 4 times - pause - retry ...'
                    UserStatusReport[email] = status,userDetails,userProject
                    print status

                # if the user was successfully assigned the _member_ role in the default project continue
                if result.status_code == 204:
                    userStatus = True
                    status = 'Step 6 - User Assigned Member Role - continue ...'
                    UserStatusReport[email] = status,userDetails,userProject
                    print status
                # if unable to assign user to default project report and exit
                else:
                    userStatus = False
                    status = 'Step 7 - Unable to  Assign User Member Role - Error, STOP!'
                    UserStatusReport[email] = status,userDetails,userProject
                    print status
            # Unable to locate default project
            else:
                userStatus = False
                status = 'Step 8 - Unable to locate default -prj project - stop and check contract details supplied...'
                UserStatusReport[email] = status,userDetails,userProject
                print status


        # if user has not been added to the central authentication portal report and exit
        else:
            status = 'Step 9 - Failed to add user to Central Authentication Portal  - Error, Stop!'
            UserStatusReport[email] = status,userDetails,userProject
            print status


    # Check if new user's project exists, create if required then add user to group
    # if user has been successfully added as _member_ to default project
    if userStatus:
        # get the project id - this will ne 'None' if the project does not exist
        newProjectid = get_itemid(get_keystoneobject_list('projects'),userProject,'projects')

        # if the users project already exists
        if (newProjectid != 'None'):
            # build my 'standard' project group name
            userGroup = userProject + '_Admin'
            # get the group id - this will be set to 'None' if the group does not exist
            defaultGroupid = get_itemid(get_keystoneobject_list('groups'),userGroup,'groups')

            # if the user's group already exists
            if (defaultGroupid != 'None'):
                result = assign_user_to_group(userDetails[2],userGroup)

                portal_sync_delay = 0

                # added a retry/delay routine here to allow sychronisation time between central portal and K5 IaaS regional portal
                while (portal_sync_delay < 4) and (result.status_code != 204):
                    time.sleep(5)
                    result = assign_user_to_group(userDetails[2],userGroup)
                    portal_sync_delay = portal_sync_delay + 1
                    status = 'Step 10 - User details not synced to IaaS portal - waiting 5 seconds before retrying up to 4 times - pause - Retry'
                    UserStatusReport[email] = status,userDetails,userProject
                    print status

            # if the users group does not exist
            else:
                # create a project admin group - enforce standards
                status = 'Step 11 - Missing Group  - Creating new user group - continue ...'
                UserStatusReport[email] = status,userDetails,userProject
                userStatus = True
                print status
                newGroup = create_new_group(userProject)

                # if the new group was created successfully
                if newGroup == (userProject + '_Admin'):
                    userStatus = True
                else:
                    userStatus = False

                result = assign_role_to_group_and_project(newGroup,userProject,"cpf_systemowner")

                portal_sync_delay = 0
                # added a retry/delay routine here to allow sychronisation time between central portal and K5 IaaS regional portal
                while (portal_sync_delay < 4) and (result.status_code != 204):
                    time.sleep(5)
                    result = assign_role_to_group_and_project(newGroup,userProject,"cpf_systemowner")
                    portal_sync_delay = portal_sync_delay + 1
                    status = 'Step 12 - Attempt to Assign Role to Group and Project Failed  - pause for portal sync, retrying....'
                    UserStatusReport[email] = status,userDetails,userProject
                    print status

                # if the new role was successfully assigned to the group and project
                if (result.status_code == 204) and (userStatus):
                    userStatus = True
                    status = 'Step 13 - Successfully Assigned role to Group  - continue...'
                    UserStatusReport[email] = status,userDetails,userProject
                    print status

                # failed to assign role to group
                else:
                    userStatus = False
                    status = 'Step 14 - Failed to Assign role to Group - STOP, ERROR!!'
                    UserStatusReport[email] = status,userDetails,userProject
                    print status

                result = assign_user_to_group(userDetails[2],newGroup)

                # if the new user was successfully assigned to the group
                if (result.status_code == 204) and (userStatus):
                    userStatus = True
                    status = 'Step 15 - Successfully Added User to Group  - continue ...'
                    UserStatusReport[email] = status,userDetails,userProject
                    print status

                # failed to add new group
                else:
                    userStatus = False
                    status = 'Step 16 - Failed to Add User to Group - Error, STOP!'
                    UserStatusReport[email] = status,userDetails,userProject
                    print status

        # if user project does not exist then create everything!
        else:
            # create new user project, group, assign role to group, assign group to project, assign user to project

            # create new project
            result = create_new_project(userProject)

            # check here for project creation status
            if result.status_code == 201:
                userStatus = True
                status = 'Step 17 - Project Created Successfully  - Status Good Continue....'
                UserStatusReport[email] = status,userDetails,userProject
                print status
            else:
                userStatus = False
                status = 'Step 18 - Project Create Failed  - Error, Stop!'
                UserStatusReport[email] = status,userDetails,userProject
                print status

            if userStatus:
                newGroup = create_new_group(userProject)

                if newGroup == (userProject + '_Admin'):
                    userStatus = True
                    status = 'Step 19 - New Group Created Successfully  - Status Good Continue....'
                    UserStatusReport[email] = status,userDetails,userProject
                    print status
                else:
                    userStatus = False
                    status = 'Step 20 - Group Create Failed  - Error, Stop!'
                    UserStatusReport[email] = status,userDetails,userProject
                    print status

                # assign role to new group and project
                result = assign_role_to_group_and_project(newGroup,userProject,"cpf_systemowner")

                portal_sync_delay = 0
                # added a retry/delay routine here to allow sychronisation time between central portal and K5 IaaS regional portal
                while (portal_sync_delay < 4) and (result.status_code != 204):
                    time.sleep(5)
                    result = assign_role_to_group_and_project(newGroup,userProject,"cpf_systemowner")
                    portal_sync_delay = portal_sync_delay + 1
                    status = 'Step 21 - Attempt to Assigned Role to Group and Project  - pause for portal sync, retrying....'
                    UserStatusReport[email] = status,userDetails,userProject
                    print status

                # if the new role was successfully assigned to the group and project
                if (result.status_code == 204) and (userStatus):
                    userStatus = True
                    status = 'Step 22 - Successfully Assigned role to Group  - continue...'
                    UserStatusReport[email] = status,userDetails,userProject
                    print status

                # failed to assign role to group
                else:
                    userStatus = False
                    status = 'Step 23 - Failed to Assign role to Group - STOP, ERROR!!'
                    UserStatusReport[email] = status,userDetails,userProject
                    print status


            if userStatus:
                userStatus = False
                status = 'Step 24 - Attempt to Assigned User to Group  - continue....'
                UserStatusReport[email] = status,userDetails,userProject

                # assign user to new group
                result = assign_user_to_group(userDetails[2],newGroup)

                portal_sync_delay = 0

                # added a retry/delay routine here to allow sychronisation time between central portal and K5 IaaS regional portal
                while (portal_sync_delay < 4) and (result.status_code != 204):
                    time.sleep(5)
                    result = assign_user_to_group(userDetails[2],newGroup)
                    portal_sync_delay = portal_sync_delay + 1
                    status = 'Step 25 - Attempt to Assigned User to Group  - pause, retrying....'
                    UserStatusReport[email] = status,userDetails,userProject
                    print status
                # check here for new group creation status
                if result.status_code == 204:
                    userStatus = True
                    status = 'Step 26 - Assigned User Successfully  - Continue....'
                    UserStatusReport[email] = status,userDetails,userProject
                    print status
                else:
                    userStatus = False
                    status = 'Step 27 - Failed to Assign User  - Error, Stop!'
                    UserStatusReport[email] = status,userDetails,userProject
                    print status


    # if user addition to default project failed
    else:
        status = 'Step 28 - Failed to assign Role to user - User Bad - Manually Complete User Addition'
        userStatus = False
        UserStatusReport[email] = status,userDetails,userProject
        print status

    userCounter = userCounter + 1
    print userDetails

#for key, value in UserStatusReport.iteritems():
#    output = 'Email: '  + value[1][3] + '\t| Login: ' + value[1][2] + '\t| Password: ' + value[1][4] + '\t | Status: ' + value[0] + '\t | Project: ' + value[2]
#    print output

if __name__ == "__main__":
    main()