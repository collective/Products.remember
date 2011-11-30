from Products.CMFCore.utils import getToolByName


def uninstall(self, portal, reinstall=False):
    setup_tool = getToolByName(portal, 'portal_setup')
    profile = "Products.remember:uninstall"

    # Revert some setup tool settings to vanilla plone values, so the tools
    # work.  This is a flimsy, because the vanilla plone settings could change,
    # but we have no real choice.  If other extensions change these settings,
    # themselves, they'll have to be reinstalled to reestablish their values.
    # Adjustment method adapted from:
    # http://plone.org/documentation/kb/manually-removing-local-persistent-utilities

    toolset = portal.portal_setup.getToolsetRegistry()
    if 'portal_registration' in toolset._required.keys():
        prdict = toolset._required['portal_registration']
        prdict['class'] = 'Products.CMFPlone.RegistrationTool.RegistrationTool'
    if 'portal_memberdata' in toolset._required.keys():
        pmdict = toolset._required['portal_memberdata']
        pmdict['class'] = 'Products.PlonePAS.tools.memberdata.MemberDataTool'

    portal.portal_controlpanel.unregisterApplication('remember')

    uninstall_profile = 'profile-%s' % profile
    setup_tool.runAllImportStepsFromProfile(uninstall_profile)
    # XXX actions.xml seems not yet implemented for uninstall profiles, and
    # when it eventually is, having what we're doing now run double won't hurt.
    setup_tool.runImportStepFromProfile(uninstall_profile, 'actions', True)
