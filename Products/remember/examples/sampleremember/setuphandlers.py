from Products.remember.utils import getAdderUtility
from config import DEFAULT_MEMBER_TYPE

def setupNewDefaultMember(context):
    """ Setup preferred default_member_type """
    portal = context.getSite()
    addr = getAdderUtility(portal)
    addr.default_member_type = DEFAULT_MEMBER_TYPE
