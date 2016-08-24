from Products.CMFCore.utils import getToolByName


def uninstall(self, portal, reinstall=False):
    setup_tool = getToolByName(portal, 'portal_setup')
    profile = "Products.remember:uninstall"

    portal.portal_controlpanel.unregisterApplication('remember')

    uninstall_profile = 'profile-%s' % profile
    setup_tool.runAllImportStepsFromProfile(uninstall_profile)
    # XXX actions.xml seems not yet implemented for uninstall profiles, and
    # when it eventually is, having what we're doing now run double won't hurt.
    setup_tool.runImportStepFromProfile(uninstall_profile, 'actions', True)
