from Products.CMFCore.utils import getToolByName

from Products.Five import BrowserView

from Products.remember.interfaces import IRememberAuthProvider

class PrefsUrlComputer(BrowserView):
    """
    Trivial view class that computes the appropriate URL for the
    'preferences' link.
    """
    def getPrefsUrl(self):
        mtool = getToolByName(self.context, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        if IRememberAuthProvider.providedBy(member):
            # we're a remember type
            return "%s/edit" % member.absolute_url()
        portal_url = getToolByName(self.context, 'portal_url')()
        return "%s/personalize_form" % portal_url
