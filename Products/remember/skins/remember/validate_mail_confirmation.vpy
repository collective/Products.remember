## Controlled Python Script "validate_mail_confirmation"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=id
##title=Validates Registration Confirmation Mail
##
from Products.CMFCore.utils import getToolByName

preg = getToolByName(context, 'portal_registration')
error_msg = preg.validateMailConfirmation(id)

if error_msg:
    state.setError('id', error_msg)
    return state.set(status='failure',
                     portal_status_message='We were unable to mail '
                     'your confirmation.')

return state
