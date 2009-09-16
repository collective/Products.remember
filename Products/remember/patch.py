from Products.CMFCore.utils import getToolByName
from Products.PlonePAS.tools.memberdata import MemberDataTool \
     as BaseTool
from Products.remember.content.member import BaseMember
from Products.remember.tools.memberdata import MemberDataContainer

# Make call to getUserName instead of getId
def wrapUser(self, user):
        """
        If possible, returns the Member object that corresponds to the
        given User object.
        """
        mbtool = getToolByName(self, 'membrane_tool')
        mem = mbtool.getUserAuthProvider(user.getUserName())
        if mem is None:
            return BaseTool.wrapUser(self, user)
        return mem.__of__(self).__of__(user)

# Make call to getId instead of getUserName
def register(self):
        """
        perform any registration information necessary after a member is registered
        """
        rtool = getToolByName(self, 'portal_registration')
        site_props = getToolByName(self, 'portal_properties').site_properties
        
        # XXX unicode names break sending the email
        unicode_name = self.getFullname()
        self.setFullname(str(unicode_name))
        if site_props.validate_email or self.getMail_me():
            rtool.registeredNotify(self.getId())

        self.setFullname(unicode_name)

# Patch validate_id to getMemberById instead of mbtool.getUserAuthProvider
# since the latter does lookups on login, not id
from Products.remember.config import ALLOWED_MEMBER_ID_PATTERN
def validate_id(self, id):
    # we can't always trust the id argument, b/c the autogen'd
    # id will be passed in if the reg form id field is blank
    form = self.REQUEST.form
    if form.has_key('id') and not form['id']:
        return self.translate('Input is required but no input given.',
                              default='You did not enter a login name.'),
    elif self.id and id != self.id:
        # we only validate if we're changing the id
        mtool = getToolByName(self, 'portal_membership')
        if mtool.getMemberById(id) is not None or \
               not ALLOWED_MEMBER_ID_PATTERN.match(id) or \
               id == 'Anonymous User':
            msg = "The login name you selected is already " + \
                  "in use or is not valid. Please choose another."
            return self.translate(msg, default=msg)

MemberDataContainer.wrapUser = wrapUser
BaseMember.register = register
BaseMember.validate_id = validate_id
