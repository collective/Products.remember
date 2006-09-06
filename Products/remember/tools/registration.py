import random, re, md5

from AccessControl import ClassSecurityInfo, getSecurityManager, \
     PermissionRole, Unauthorized
from Globals import InitializeClass
from DateTime import DateTime

from Products.CMFDefault.RegistrationTool import _checkEmail
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

    def validateMailConfirmation(self, id):
        """Validate before mailing the registration confirmation key
        to the member's email."""
        membership = getToolByName(self, 'portal_membership')
        member = membership.getMemberById(id)

        if member is None:
            return 'The username you entered could not be found.'

        wft = getToolByName(self, 'portal_workflow')
        if wft.getInfoFor(member, 'review_state') != 'unconfirmed':
            return 'This user has already been confirmed.'

        if (membership.confirm_expire and
            DateTime() - member.created() > membership.confirm_expire):
            return 'Your registration has expired.'

        # assert that we can actually get an email address, otherwise
        # the template will be made with a blank To:, this is bad
        if not member.getProperty('email'):
            return 'That user does not have an email address.'

        check, msg = _checkEmail(member.getProperty('email'))
        if not check:
            return msg

    def mailConfirmation(self, id):
        """Send a mail with the confirmation key."""
        # Rather than have the template try to use the mailhost, we will
        # render the message ourselves and send it from here (where we
        # don't need to worry about 'UseMailHost' permissions).
        membership = getToolByName(self, 'portal_membership')
        member = membership.getMemberById(id)

        mail_text = self.mail_confirmation_template(
            member_id=member.getId(),
            member_email=member.getProperty('email'),
            confirmationKey=member.getConfirmationKey())

        host = self.MailHost
        host.send(mail_text)

InitializeClass(RegistrationTool)
