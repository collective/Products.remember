## Script (Python) "searchMember"
##title=Edit content
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=type_name=None, came_from_prefs=None

request = context.REQUEST.form

if 'the_cb_is_checked' in request:
    request['getLast_login_time_usage'] = 'range:max'
else:
    request['getLast_login_time_usage'] = 'range:min'

return state
