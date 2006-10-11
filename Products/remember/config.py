"""
remember

A membrane-based Plone member implementation.

$Id$
"""
import re

__authors__ = 'Rob Miller',
__docformat__ = 'text/restructured'

PROJECT_NAME           = 'remember'
SKINS_DIR              = 'skins'
GLOBALS                = globals()

DEFAULT_MEMBER_TYPE = 'Member'

ALLOWED_MEMBER_ID_PATTERN = re.compile( "^[A-Za-z][A-Za-z0-9_]*$" )

AUTO_ROLES = ('Anonymous', 'Authenticated')

ANNOT_KEY = 'Products.remember'

HASHERS = ['bcrypt', 'hmac_sha', 'zauth', 'sha']

CMFMEMBER_MIGRATION_SUPPORT = False
