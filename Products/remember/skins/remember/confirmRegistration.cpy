## Script (Python) "confirmMember"
##title=Confirm a Member Registration
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
from Products.CMFCore.utils import getToolByName

wft = getToolByName(context, 'portal_workflow')
wft.doActionFor(context,'register_public')

purl = getToolByName(context, 'portal_url')

return state.set(
    context=purl.getPortalObject(),
    portal_status_message='Your registration has been confirmed, '
    'please login.')
