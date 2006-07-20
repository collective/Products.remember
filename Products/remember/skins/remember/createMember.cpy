## Script (Python) "createMember"
##title=Edit content
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=type_name=None, came_from_prefs=None
from DateTime import DateTime
from Products.CMFPlone import transaction_note

now=DateTime()

mdc = context.portal_memberdata

if not type_name:
    type_name = mdc.getDefaultType()

id=context.generateUniqueId(type_name)

mem = mdc.restrictedTraverse('portal_factory/%s/%s' % (type_name, id))
transaction_note('Initiated creation of %s with id %s in %s' % (mem.getTypeInfo().getId(),
                                                                id,
                                                                context.absolute_url()))
return state.set(context=mem)
