import types
from os.path import join, abspath, dirname

import ZConfig

from config import AUTO_ROLES

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
