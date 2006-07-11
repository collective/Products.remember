import types
from os.path import join, abspath, dirname

import ZConfig

from config import AUTO_ROLES

import logging
logger = logging.getLogger('remember')

def stringToList(s):
    if s is None:
        return []
    if isinstance(s, types.StringType):
        # split on , or \n and ignore \r
        s = s.replace('\r',',')
        s = s.replace('\n',',')
        s = s.split(',')
    s= [v.strip() for v in s if v.strip()]
    return [o for o in s if o]

def removeAutoRoles(roles_list):
    """ removes automatic roles from passed in list """
    for auto_role in AUTO_ROLES:
        while auto_role in roles_list:
            roles_list.remove(auto_role)

DIR_PATH = abspath(dirname(__file__))

def conf_file(file):
    return join(DIR_PATH, 'conf', file)

def parseDependencies():
    schema = ZConfig.loadSchema(conf_file('depends.xml'))
    config, handler = ZConfig.loadConfig(schema,
                                         conf_file('depends.conf'))
    return config, handler

def log(message, summary='', severity=logging.INFO):
    logger.log(severity, '%s \n%s', summary, message)

def log_exc():
    """Dump an exception to the log"""
    import traceback
    import sys

    s = sys.exc_info()[:2]  # don't assign the traceback to s (otherwise will generate a circular reference)
    if s[0] == None:
        summary = 'None'
    else:
        if type(s[0]) == type(''):
            summary = s[0]
        else:
            summary = str(s[1])

    logger.log(logging.ERROR, '%s \n%s', summary, '\n'.join(traceback.format_exception(*sys.exc_info())))
