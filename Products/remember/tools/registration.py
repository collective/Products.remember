import random, re, md5

from AccessControl import ClassSecurityInfo, getSecurityManager, \
     PermissionRole, Unauthorized
from Globals import InitializeClass

from Products.CMFCore.utils import getToolByName, _checkPermission
from Products.CMFCore import CMFCorePermissions
from Products.CMFPlone.RegistrationTool import RegistrationTool as BaseTool

from Products.remember.permissions import MAIL_PASSWORD_PERMISSION

# - remove '1', 'l', and 'I' to avoid confusion
# - remove '0', 'O', and 'Q' to avoid confusion
# - remove vowels to avoid spelling words
invalid_password_chars = ['a','e','i','o','u','y','l','q']

def getValidPasswordChars():
    password_chars = []
    for i in range(0, 26):
        if chr(ord('a')+i) not in invalid_password_chars:
            password_chars.append(chr(ord('a')+i))
            password_chars.append(chr(ord('A')+i))
    for i in range(2, 10):
        password_chars.append(chr(ord('0')+i))
    return password_chars

password_chars = getValidPasswordChars()


# seed the random number generator
random.seed()


class RegistrationTool(BaseTool):
    meta_type='remember Registration Tool'
    security = ClassSecurityInfo()

    security.declarePublic('testPasswordValidity')
    def testPasswordValidity(self, password, confirm=None):
        """ Verify that the password satisfies the portal's requirements.

        o If the password is valid, return None.
        o If not, return a string explaining why.

        Comparison of password and confirm handled in Member.post_validate.
        """
        if len(password) < 5 and not _checkPermission('Manage portal', self):
            return self.translate('help_password_creation',
                                  default='Passwords must contain at least ' +
                                          '5 characters.')
        return None


    # A replacement for portal_registration's mailPassword function
    # The replacement secures the mail password function with
    # MAIL_PASSWORD_PERMISSION so that members can be disabled.
    security.declarePublic('mailPassword')
    def mailPassword(self, forgotten_userid, REQUEST):
        """ Email a forgotten password to a member.
        
        o Raise an exception if user ID is not found.
        
        """
        membership_tool = getToolByName(self, 'portal_membership')
        member = membership_tool.getMemberById(forgotten_userid)

        if member is None:
            raise ValueError, 'The username you entered could not be found'

        # we have to do our own security check since we are in a tool
        # and bypassing Zope security; we can't call member.mailPassword
        # directly since in private state it's not viewable by anonymous
        necessary_roles = PermissionRole.rolesForPermissionOn(MAIL_PASSWORD_PERMISSION, member)
        for role in getSecurityManager().getUser().getRolesInContext(member):
            if role in necessary_roles:
                return BaseTool.mailPassword(self, forgotten_userid, REQUEST)
        raise(Unauthorized)


InitializeClass(RegistrationTool)
