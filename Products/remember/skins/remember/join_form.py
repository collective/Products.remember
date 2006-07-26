## Script (Python) "join_form"
##title=Edit content
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=type_name=None
url = "%s/createMember" % context.portal_url()
if type_name is not None:
    url += "?type_name=%s" % type_name
context.REQUEST.RESPONSE.redirect(url)
