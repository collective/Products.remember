from Products.Archetypes import public as atapi
from Products.CMFCore import permissions as cmfcore_permissions

import config

# This file is used to set up permissions for your product.
 
# Add a new member
ADD_PERMISSION = ADD_MEMBER_PERMISSION = cmfcore_permissions.AddPortalMember
# Register a new member, i.e. "activate" a membership
REGISTER_PERMISSION = 'membrane: Register member'
# Disable a membership
DISABLE_PERMISSION = cmfcore_permissions.ManageUsers
# Modify the member's ID -- should only happen during preregistration
EDIT_ID_PERMISSION = 'membrane: Edit member id'
# Modify the member's general properties
EDIT_PROPERTIES_PERMISSION = cmfcore_permissions.SetOwnProperties
# Change a member's password
EDIT_PASSWORD_PERMISSION = cmfcore_permissions.SetOwnPassword
# Change a member's roles and domains
EDIT_SECURITY_PERMISSION = cmfcore_permissions.ManageUsers
# Appear in searches
VIEW_PERMISSION = cmfcore_permissions.View
# View a member's roles and domains
VIEW_SECURITY_PERMISSION = cmfcore_permissions.ManageUsers
# View a member's public information
VIEW_PUBLIC_PERMISSION = VIEW_PERMISSION
# View a member's private information
VIEW_OTHER_PERMISSION = EDIT_PROPERTIES_PERMISSION
# Enable password mailing
MAIL_PASSWORD_PERMISSION = cmfcore_permissions.MailForgottenPassword


# The code below will create a unique add permission for each of your
# content types.  The permission for adding the type MyContentType will
# be 'MyProject: Add MyContentType'.  If instead you want to specify
# your own add permission (e.g. use the CMF's 'Add portal content'
# permission), you can use the ADD_PERMISSIONS dictionary to do so.

# ADD_PERMISSIONS is used to specify the name of the permission
# used for adding one of your content types.  For example:
#
# ADD_PERMISSIONS = {'MyFirstContentType': 'Add portal content',
#                    'MySecondContentType': 'My other permission',
#                   }

# XXX Hard-coded the 'Member' type to prevent circular import
ADD_PERMISSIONS = {'Member': ADD_MEMBER_PERMISSION,
                   }

# The SITEWIDE_PERMISSIONS dictionary is used for assigning permissions
# to different roles site-wide.  For example, if you create the new roles
# 'Czar' and 'Peasant', you could give them the 'Add portal folders' and
# 'Delete objects' permissions like so:
#
# SITEWIDE_PERMISSIONS = (
#    (['Czar', 'Peasant'], ['Add portal folders', 'Delete objects'']),
#   )
#
# In general, the pattern is
#
# SITEWIDE_PERMISSIONS = ( 
#   ([list of roles], [list of permissions]),
#   ([second list of roles], [second list of permissions]),
#  )
#
# The site-wide permissions are set in Extensions/Install.py

SITEWIDE_PERMISSIONS = ()


def initialize():
    permissions = {}
    types = atapi.listTypes(config.PROJECT_NAME)
    for atype in types:
        portal_type = atype['portal_type']
        permission = ADD_PERMISSIONS.get(portal_type, None)
        if permission is None:
            # construct a permission on the fly
            permission = "%s: Add %s" % (config.PROJECT_NAME,
                                         portal_type)
            cmfcore_permissions.setDefaultRoles(permission, ('Manager',))
        permissions[portal_type] = permission

    return permissions
