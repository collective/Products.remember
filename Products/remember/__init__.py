#{Header, text, replace}#
"""
remember

A membrane-based Plone member implementation.

$Id$
"""
__authors__ = 'Rob Miller',
__docformat__ = 'text/restructured'

# __init__.py is used to register global tools, services, and
# configuration information

import sys

from OFS.Image import Image

from Products.Archetypes import public as atapi
from Products.CMFCore import utils as cmf_utils
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFPlone.interfaces import IPloneSiteRoot

from Products.PlonePAS.sheet import PropertySchema

from Products.GenericSetup import EXTENSION
from Products.GenericSetup import profile_registry

from permissions import initialize as initialize_permissions
import config

if config.CMFMEMBER_MIGRATION_SUPPORT:
    import cmfmember
    from cmfmember.migrator import registerMigrators

# BBB from when we had a custom membership tool
sys.modules['Products.remember.tools.membership'] = \
        sys.modules['Products.PlonePAS.tools.membership']

# Register the skins directory
registerDirectory(config.SKINS_DIR, config.GLOBALS)

def initialize(context):
    # register the CMFMember migrators, if necessary
    if config.CMFMEMBER_MIGRATION_SUPPORT:
        registerMigrators()
    
    # Importing the content types allows for their registration
    # with the Archetypes runtime
    import content

    # Ask Archetypes to handback all the type information needed
    # to make the CMF happy.
    types = atapi.listTypes(config.PROJECT_NAME)
    content_types, constructors, ftis = \
        atapi.process_types(types, config.PROJECT_NAME)

    # We register each type with an add permission that is set
    # in permissions.py.  By default, each content type has its
    # own permission, but this behavior can be easily overridden.
    permissions = initialize_permissions()
    allTypes = zip(content_types, constructors)
    for atype, constructor in allTypes:
        kind = "%s: %s" % (config.PROJECT_NAME, atype.archetype_name)
        cmf_utils.ContentInit(
            kind,
            content_types      = (atype,),
            permission         = permissions[atype.portal_type],
            extra_constructors = (constructor,),
            fti                = ftis,
            ).initialize(context)


    profile_desc = "Installs membrane-based Plone member implementation."
    profile_registry.registerProfile('default',
                                     'remember',
                                     profile_desc,
                                     'profiles/default',
                                     'remember',
                                     EXTENSION,
                                     for_=IPloneSiteRoot,
                                     )

    # register image property type for user property sheets
    PropertySchema.addType('image',
                           lambda x: x is None or isinstance(x, Image))
