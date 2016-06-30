import logging
from Products.CMFCore.utils import getToolByName

from Products.PluggableAuthService.interfaces.plugins \
    import IUserAdderPlugin

from Products.remember.pas import install as pas_install
from zope.component import getUtility
from Products.CMFCore.interfaces import ISiteRoot

logger = logging.getLogger("Products.remember")
PROFILE_ID = 'profile-Products.remember:default'


def remove_old_import_steps(context):
    # context is portal_setup which is nice
    registry = context.getImportStepRegistry()
    old_steps = ('portal_form_controller', 'remember-setupplugins')
    for old_step in old_steps:
        if old_step in registry.listSteps():
            registry.unregisterStep(old_step)

            # Unfortunately we manually have to signal the context
            # (portal_setup) that it has changed otherwise this change is
            # not persisted.
            #context._p_changed = True
            logger.info("Old %s import step removed from persistent import "
                        "registry.", old_step)


def keyword_index_get_roles(context):
    """Change the getRoles index into a KeywordIndex.

    It used to be a FieldIndex.
    """
    membrane_tool = getToolByName(context, 'membrane_tool')
    try:
        getRoles = membrane_tool.Indexes['getRoles']
    except KeyError:
        getRoles = None
    else:
        if getRoles.meta_type != 'KeywordIndex':
            membrane_tool.manage_delIndex('getRoles')
            logger.info("Removed index getRoles with type %s.",
                        getRoles.meta_type)
            getRoles = None

    if getRoles is None:
        # Index was not there or has just been removed because it was
        # of the wrong type.
        membrane_tool.addIndex('getRoles', 'KeywordIndex')
        logger.info("Added KeywordIndex for field getRoles.")
        logger.info("Indexing index getRoles.")
        membrane_tool.manage_reindexIndex(ids='getRoles')


def setupPlugins(context):
    """ initialize membrane plugins """
    if context.readDataFile('remember-setup-plugins.txt') is None:
        return

    portal = context.getSite()
    uf = getToolByName(portal, 'acl_users')
    plugins = uf.plugins

    # Make sure that the UserAdding is handled by membrane
    plugins.movePluginsUp(IUserAdderPlugin, ['membrane_users'])
    # Install and activate the email login auth extraction handler:
    setupEmailPASPlugin(context)


def setupEmailPASPlugin(context):
    """ Activate the email auth PAS plugin """
    pas_install.activate_pas_plugin(getUtility(ISiteRoot).acl_users,
                                    'remember_email_auth',
                                    "Remember Email User Authentication")


def apply_toolset_step(context):
    context.runImportStepFromProfile(PROFILE_ID, 'toolset')


def apply_memberdata_properties_step(context):
    context.runImportStepFromProfile(PROFILE_ID, 'memberdata-properties')
