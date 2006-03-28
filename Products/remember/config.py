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

ALLOWED_MEMBER_ID_PATTERN = re.compile( "^[A-Za-z][A-Za-z0-9_]*$" )

AUTO_ROLES = ('Anonymous', 'Authenticated')
