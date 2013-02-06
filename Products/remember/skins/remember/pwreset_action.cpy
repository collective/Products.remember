## Script (Python) "pwreset_action.cpy"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Reset a user's password
##parameters=randomstring, userid=None, password=None, password2=None
from Products.CMFCore.utils import getToolByName
from Products.remember.pas.utils import getUserIdForEmail
from Products.remember.pas.utils import email_login_is_active

status = "success"
pw_tool = getToolByName(context, 'portal_password_reset')
if '@' in userid and email_login_is_active():
    userid = getUserIdForEmail(context, userid) or userid
try:
    pw_tool.resetPassword(userid, randomstring, password)
except 'ExpiredRequestError':
    status = "expired"
except 'InvalidRequestError':
    status = "invalid"
except RuntimeError:
    status = "invalid"
except ValueError:
    status = "invalid"

return state.set(status=status)

