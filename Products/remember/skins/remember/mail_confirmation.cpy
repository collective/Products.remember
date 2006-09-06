## Script (Python) "mail_confirmation"
##title=Mail a Registration Confirmation Key
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=id
from Products.CMFCore.utils import getToolByName

preg = getToolByName(context, 'portal_registration')
preg.mailConfirmation(id)

return state.set(
    portal_status_message='Your registration confirmation key has '
    'been mailed.')
