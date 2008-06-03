from Products.CMFCore.utils import getToolByName

from Products.PluggableAuthService.interfaces.plugins \
     import IUserAdderPlugin


def setupPlugins(context):
    """ initialize membrane plugins """
    if context.readDataFile('remember-setup-plugins.txt') is None:
        return

    portal = context.getSite()
    uf = getToolByName(portal, 'acl_users')
    plugins = uf.plugins

    # Make sure that the UserAdding is handled by membrane
    plugins.movePluginsUp(IUserAdderPlugin, ['membrane_users'])

