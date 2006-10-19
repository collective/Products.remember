from Products.membrane.setuphandlers import _membraneProfileActive
from Products.membrane.setuphandlers import _doRegisterUserAdderUtility

from utilities import UserAdder
from config import ADDUSER_UTILITY_NAME

PROFILE_ID = "profile-remember:default"

def registerUserAdderUtility(context):
    """ registers the remember IUserAdder utility """
    _doRegisterUserAdderUtility(context, 'remember-useradder',
                                PROFILE_ID, ADDUSER_UTILITY_NAME,
                                UserAdder())

