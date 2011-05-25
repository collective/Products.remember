from Products.CMFCore.utils import getToolByName
from Products.remember.setuphandlers import uninstall

def uninstall(self, portal, reinstall=False):
    setup_tool = getToolByName(portal, 'portal_setup')
    profile = "remember:uninstall"

    # Revert some setup tool settings to vanilla plone values, so the tools
    # work.  This is a flimsy, because the vanilla plone settings could change,
    # but we have no real choice.  If other extensions change these settings,
    # themselves, they'll have to be uninstalled and reinstalled to reestablish
    # their values.  Adjustment method adapted from:
#http://plone.org/documentation/kb/manually-removing-local-persistent-utilities

    toolset = portal.portal_setup.getToolsetRegistry()
    if toolset._required.has_key('portal_registration'):
        prdict = toolset._required['portal_registration']
        prdict['class'] = 'Products.CMFPlone.RegistrationTool.RegistrationTool'
    if toolset._required.has_key('portal_memberdata'):
        pmdict = toolset._required['portal_memberdata']
        pmdict['class'] = 'Products.PlonePAS.tools.memberdata.MemberDataTool'

    portal.portal_controlpanel.unregisterApplication('remember')

    setup_tool.runAllImportStepsFromProfile('profile-%s' % profile)
