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
new_context = context.portal_factory.doCreate(context, id)
new_context.processForm()

from AccessControl import Unauthorized

try:
     userCreated = new_context.hasUser()
except Unauthorized: # <-- member has been made pending
     userCreated = False

portal = new_context.portal_url.getPortalObject()
state.setContext(portal)

if came_from_prefs:
     state.set(status='prefs', portal_status_message='User added.')
elif userCreated:
     state.set(status='success',
               portal_status_message='You have been registered.',
               id=id,
               password=password)
else:
     state.set(status='pending',
               portal_status_message='Your registration request has been received')

return state
