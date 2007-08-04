"""Various extensions based on remember for supporting different
portal membership types and policies."""

from Products.Archetypes import public as atapi
from Products.CMFCore import utils as cmf_utils
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFPlone.interfaces import IPloneSiteRoot

from Products.GenericSetup import EXTENSION
from Products.GenericSetup import profile_registry

from Products.sampleremember import config
from permissions import initialize as initialize_permissions

# Register the skins directory
registerDirectory(config.SKINS_DIR, config.GLOBALS)

def initialize(context):
    # Importing the content types allows for their registration
    # with the Archetypes runtime
    from Products.sampleremember import content

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

    profile_registry.registerProfile(
        'default',
        'sampleremember',
        "Installs sampleremember.",
        'profiles/default',
        'sampleremember',
        EXTENSION,
        for_=IPloneSiteRoot,)