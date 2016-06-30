from AccessControl.Permissions import manage_users
from Products.CMFCore.utils import getToolByName
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService import registerMultiPlugin

from interface import IRememberEmailAuth
from zExceptions import BadRequest

import plugin

manage_add_pas_form = PageTemplateFile('browser/add_plugin',
                                       globals(), __name__='manage_add_pas_form')


def manage_add_remember_emaillogin_user_authentication(dispatcher, id,
                                                       title=None,
                                                       REQUEST=None):
    """Add Remember Email User Authentication to the PluggableAuthentication
    Service."""
    sp = plugin.RememberEmailAuth(id, title)
    dispatcher._setObject(sp.getId(), sp)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect('%s/manage_workspace'
                                     '?manage_tabs_message='
                                     'RememberEmailAuth+added.'
                                     % dispatcher.absolute_url())


def register_pas_plugin():
    try:
        registerMultiPlugin(plugin.RememberEmailAuth.meta_type)
    except RuntimeError:
        # make refresh users happy
        pass


def register_pas_plugin_class(context):
    context.registerClass(plugin.RememberEmailAuth,
                          permission=manage_users,
                          constructors=(manage_add_pas_form,
                                        manage_add_remember_emaillogin_user_authentication),
                          visibility=None,
                          icon='pas/browser/icon.gif')


def activate_pas_plugin(context, id, title):
    try:
        manage_add_remember_emaillogin_user_authentication(context, id, title)
        plugin = getattr(context, id)
        plugin.manage_activateInterfaces(('IExtractionPlugin',))
    except (RuntimeError, BadRequest):
        # don't complain on refresh or already-present:
        pass
