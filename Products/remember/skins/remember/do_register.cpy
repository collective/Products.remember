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

new_context = context.portal_factory.doCreate(context, id)
new_context.processForm()

portal = new_context.portal_url.getPortalObject()
state.setContext(portal)

wft = getToolByName(new_context, 'portal_workflow')
review_state = wft.getInfoFor(new_context, 'review_state')

if came_from_prefs:
     state.set(status='prefs', portal_status_message='User added.')

# Access to hasUser is protected by View which is not available on
# workflows other than member_auto_workflow
elif review_state in ('public', 'private') and new_context.hasUser():
     state.set(status='success',
               portal_status_message='You have been registered.',
               id=id,
               password=password)

elif review_state == 'unconfirmed':
     state.set(status='unconfirmed',
               portal_status_message='You must now confirm your '
               'registration.') 

elif review_state == 'pending':
     state.set(status='pending',
               portal_status_message='Your registration request has '
               'been received')

else:
     raise ValueError, ('Member workflow state %s not handled by '
                        'do_register.' % review_state)

return state
