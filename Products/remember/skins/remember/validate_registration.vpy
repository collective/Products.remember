## Controlled Python Script "validate_registration"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=id=None,password=None,mail_me=None,fieldset=None
##title=Validates registration
##
fields = []
testid = None
testpwd = None

if fieldset is not None:
    schemata = context.Schemata()[fieldset]
    fields = schemata.fields()
    fieldnames = schemata.keys()
else:
    fields += context.Schema().filterFields(isMetadata=0)
    fieldnames = [field.getName() for field in fields]

if 'id' in fieldnames:
    testid = 1

if 'password' in fieldnames:
    testpwd = 1

if testid and not id:
    state.setError('id', 'You did not enter a username.', 'invalid_id')

properties = context.portal_properties.site_properties
if not properties.validate_email and testpwd and not password and not mail_me:
    state.setError('password',
                   'You must enter a password or choose to have one mailed to you.',
                   'invalid_password')
    state.setError('mail_me', 'You must enter a password or choose to have one mailed to you.',
                   'invalid_mail_me')

if state.getErrors():
    return state.set(status='failure',
                     portal_status_message='Please correct the indicated errors')
else:
    return state
