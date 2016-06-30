from Acquisition import aq_parent
from ZTUtils import make_query

from Products.CMFCore.utils import getToolByName

from Products.remember.interfaces import IRememberAuthProvider


class PortalPrefsUrl(object):
    """
    Trivial view class that computes the appropriate URL for the
    'preferences' link for the current user.
    """

    def __call__(self):
        mtool = getToolByName(self.context, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        if IRememberAuthProvider.providedBy(member):
            # we're a remember type
            return "%s/edit" % member.absolute_url()
        portal_url = getToolByName(self.context, 'portal_url')()
        return "%s/personalize_form" % portal_url


class RememberPrefsUrl(object):
    """
    Trivial view class that computes the appropriate URL for the
    'preferences' link for a remember user.
    """

    def __call__(self):
        return self.context.absolute_url()


class MemberPrefsUrl(object):
    """
    Trivial view class that computes the appropriate URL for the
    'preferences' link for a non-remember user.
    """

    def __call__(self):
        member = aq_parent(self.context)
        portal_url = getToolByName(self.context, 'portal_url')()
        return "%s/@@user-information?%s" % (
            portal_url, make_query(userid=member.getUserId()))


class BBBMemberPrefsUrl(object):
    """
    Trivial view class that computes the appropriate URL for the
    'preferences' link for a non-remember user.
    """

    def __call__(self):
        member = aq_parent(aq_parent(self.context))
        portal_url = getToolByName(self.context, 'portal_url')()
        return "%s/prefs_user_details?%s" % (
            portal_url, make_query(userid=member.getUserId()))
