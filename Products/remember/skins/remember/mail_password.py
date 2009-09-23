## Script (Python) "mail_password"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Mail a user's password
##parameters=

from Products.CMFPlone import PloneMessageFactory as pmf
from Products.remember.pas.utils import getUserIdForEmail
from Products.remember.pas.utils import email_login_is_active

REQUEST=context.REQUEST
userid = REQUEST['userid']
if '@' in userid and email_login_is_active():
    userid = getUserIdForEmail(context, userid) or userid
try:
    response = context.portal_registration.mailPassword(userid, REQUEST)
except ValueError, e:
    context.plone_utils.addPortalMessage(pmf(str(e)))
    response = context.mail_password_form()
return response
