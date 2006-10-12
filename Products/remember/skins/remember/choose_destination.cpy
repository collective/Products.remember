## Controlled Python Script "choose_destination"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Decides where to traverse to at the end of a member edit process
##

if context.REQUEST.get('fieldset', None) == 'metadata':
    return state.set(status='view')
else:
    return state.set(status='edit')
