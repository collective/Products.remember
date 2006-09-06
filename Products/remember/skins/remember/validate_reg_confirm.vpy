## Controlled Python Script "validate_reg_confirm"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=id,confirmationKey
##title=Validates Registration Confirmation
##
from DateTime import DateTime

from Products.CMFCore.utils import getToolByName

pmem = getToolByName(context, 'portal_membership')
member = pmem.getMemberById(id)

wft = getToolByName(context, 'portal_workflow')

error_msg = 'Unable to confirm your registration.'

if member is None:
    return state.set(
        status='failure',
        errors={'id': 'User name could not be found.'},
        portal_status_message=error_msg)

if wft.getInfoFor(member, 'review_state') != 'unconfirmed':
    return state.set(
        status='failure',
        errors={'id': 'This user has already been confirmed.'},
        portal_status_message=error_msg)

if (pmem.confirm_expire and
    DateTime() - member.created() > pmem.confirm_expire):
    return state.set(
        status='failure',
        errors={'confirmationKey': 'Your registration has expired.'},
        portal_status_message=error_msg)

if confirmationKey != member.getConfirmationKey():
    return state.set(
        status='failure',
        errors={'confirmationKey': 'The registration confirmation key is '
                'incorrect, please check your key.'},
        portal_status_message=error_msg)

return state.set(context=member)
