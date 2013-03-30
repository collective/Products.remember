import types
from os.path import join, abspath, dirname

import logging
logger = logging.getLogger('remember')

from AccessControl import ModuleSecurityInfo
from AccessControl import Unauthorized
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.SpecialUsers import system as system_user

from Products.CMFCore.utils import getToolByName

from Products.membrane.config import TOOLNAME as MBTOOLNAME
from Products.membrane.interfaces import IUserAdder

from config import AUTO_ROLES
from config import ADDUSER_UTILITY_NAME
from zope.lifecycleevent.interfaces import IObjectRemovedEvent


security = ModuleSecurityInfo('Products.remember.utils')


def getRememberTypes(context):
    """
    Return a list of all the membrane types that implement IReMember.
    """
    mbtool = getToolByName(context, MBTOOLNAME)
    return mbtool.listMembraneTypes()
security.declarePublic('getRememberTypes')


def getAdderUtility(context):
    """
    Return the local remember adder utility.
    """
    portal = getToolByName(context, 'portal_url').getPortalObject()
    sm = portal.getSiteManager()
    adder = sm.queryUtility(IUserAdder, ADDUSER_UTILITY_NAME)
    if adder is None:
        raise(RuntimeError, "Unable to retrieve IUserAdder utility")
    return adder
security.declarePublic('getAdderUtility')


def stringToList(s):
    if s is None:
        return []
    if isinstance(s, types.StringType):
        # split on , or \n and ignore \r
        s = s.replace('\r', ',')
        s = s.replace('\n', ',')
        s = s.split(',')
    s = [v.strip() for v in s if v.strip()]
    return [o for o in s if o]


def removeAutoRoles(roles_list):
    """ removes automatic roles from passed in list """
    for auto_role in AUTO_ROLES:
        while auto_role in roles_list:
            roles_list.remove(auto_role)

DIR_PATH = abspath(dirname(__file__))


def conf_file(file):
    return join(DIR_PATH, 'conf', file)


def log(message, summary='', severity=logging.INFO):
    logger.log(severity, '%s \n%s', summary, message)


def log_exc():
    """Dump an exception to the log"""
    import traceback
    import sys

    # don't assign the traceback to s
    # (otherwise will generate a circular reference)
    s = sys.exc_info()[:2]
    if s[0] == None:
        summary = 'None'
    else:
        if type(s[0]) == type(''):
            summary = s[0]
        else:
            summary = str(s[1])

    logger.log(logging.ERROR, '%s \n%s', summary,
               '\n'.join(traceback.format_exception(*sys.exc_info())))


def fixOwnership(ob, event):
    if not IObjectRemovedEvent.providedBy(event):
        ob.fixOwnership()


def trusted(fn):
    """
    Executes the callable as a Zope superuser if original call raises
    Unauthorized.
    """
    def trusted_fn(*args, **kwargs):
        try:
            value = fn(*args, **kwargs)
        except Unauthorized:
            orig_sec_mgr = getSecurityManager()
            newSecurityManager(None, system_user)
            value = fn(*args, **kwargs)
            setSecurityManager(orig_sec_mgr)
        return value
    return trusted_fn
