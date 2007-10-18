## Script (Python) "prefs_user_manage"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=users=[], resetpassword=[], delete=[]
##title=Edit users
##

from Products.CMFPlone import PloneMessageFactory as _

acl_users = context.acl_users
mtool = context.portal_membership
getMemberById = mtool.getMemberById
mailPassword = context.portal_registration.mailPassword
setMemberProperties = context.plone_utils.setMemberProperties
generatePassword = context.portal_registration.generatePassword

for user in users:
    # Don't bother if the user will be deleted anyway
    if user.id in delete:
        continue

    member = getMemberById(user.id)
    if hasattr(user, 'email'):
        # If email address was changed, set the new one
        if user.email != member.getProperty('email'):
            setMemberProperties(member, email=user.email)

    # If reset password has been checked email user a new password
    if hasattr(user, 'resetpassword'):
        pw = generatePassword()
    else:
        pw = None
    
    member.update(password=pw, roles=user.get('roles',[]))
    if pw:
        try:
            mailPassword(user.id, context.REQUEST)
        except Exception, e:
            msg = _(u'Password update for %s failed. %s' % (user.id, e))
            context.plone_utils.addPortalMessage(msg)
            

if delete:
    # BBB We should eventually have a global switch to determine member area
    # deletion
    mtool.deleteMembers(delete, delete_memberareas=0, delete_localroles=1)

context.plone_utils.addPortalMessage(_(u'Changes applied.'))
return state
