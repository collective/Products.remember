def uninstall(self, portal, reinstall=False):
    profile = "remember:uninstall"
    portal.portal_setup.runAllImportStepsFromProfile('profile-%s' % profile)
    