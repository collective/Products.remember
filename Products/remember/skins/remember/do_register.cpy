## Script (Python) "do_register"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=id, password=None, came_from_prefs=None
##title=Registered
##
#next lines pulled from Archetypes' content_edit.cpy
from Products.CMFCore.utils import getToolByName

new_context = getToolByName(context, 'portal_factory').doCreate(context, id)
new_context.processForm()

wftool = getToolByName(new_context, 'portal_workflow')
review_state = wftool.getInfoFor(new_context, 'review_state')

portal = getToolByName(new_context, 'portal_url').getPortalObject()
state.setContext(portal)

if came_from_prefs:
     state.set(status='prefs', portal_status_message='User added.')
elif review_state == 'pending':
     state.set(status='pending',
               portal_status_message='Your registration request has been received')
else:
     state.set(status='success',
               portal_status_message='You have been registered.',
               id=id,
               password=password)

return state
