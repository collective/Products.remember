## Script (Python) "searchMember"
##title=Edit content
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=type_name=None, came_from_prefs=None

form = context.REQUEST.form

if 'before_specified_time' in form:
    form['getLast_login_time_usage'] = 'range:max'
else:
    form['getLast_login_time_usage'] = 'range:min'

return state
