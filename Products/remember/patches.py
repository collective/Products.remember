from Products.CMFCore.utils import getToolByName
from Products.PasswordResetTool.PasswordResetTool import PasswordResetTool

# Use user.getUserName() and not stored_user
# The issue is reported at http://plone.org/products/passwordresettool/issues/12 
def resetPassword(self, userid, randomstring, password):
        """Set the password (in 'password') for the user who maps to
        the string in 'randomstring' iff the entered 'userid' is equal
        to the mapped userid. (This can be turned off with the
        'toggleUserCheck' method.)

        Note that this method will *not* check password validity: this
        must be done by the caller.

        Throws an 'ExpiredRequestError' if request is expired.
        Throws an 'InvalidRequestError' if no such record exists,
        or 'userid' is not in the record.
        """
        try:
            stored_user, expiry = self._requests[randomstring]
        except KeyError:
            raise 'InvalidRequestError'
        
        if self.checkUser() and (userid != stored_user):
            raise 'InvalidRequestError'
        if self.expired(expiry):
            del self._requests[randomstring]
            self._p_changed = 1
            raise 'ExpiredRequestError'

        member = self.getValidUser(stored_user)
        if not member:
            raise 'InvalidRequestError'

        # actually change password
        user = member.getUser()
        uf = getToolByName(self, 'acl_users')
        if getattr(uf, 'userSetPassword', None) is not None:
            uf.userSetPassword(user.getUserName(), password)  # GRUF 3
        else:
            try:
                user.changePassword(password)  # GRUF 2
            except AttributeError:
                # this sets __ directly (via MemberDataTool) which is the usual
                # (and stupid!) way to change a password in Zope
                member.setSecurityProfile(password=password)

        member.setMemberProperties(dict(must_change_password=0))

        # clean out the request
        del self._requests[randomstring]
        self._p_changed = 1

PasswordResetTool.resetPassword = resetPassword
