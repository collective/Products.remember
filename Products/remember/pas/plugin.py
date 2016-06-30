"""Class: RememberEmailAuth
"""

import logging

from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements

from Products.remember.pas import interface
from Products.remember.pas.utils import getBrainsForEmail

from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('Products.remember.pas.plugin')


class RememberEmailAuth(BasePlugin):
    """Multi-plugin to login remember users with their email address.

    Taken partly from betahaus.emaillogin.
    """

    meta_type = 'Remember Email User Authentication'
    security = ClassSecurityInfo()

    def __init__(self, id, title=None):
        self._setId(id)
        self.title = title

    def site_policy_allows_email_login(self):
        """
        True if Security settings allows 'Use email address as login name'.
        """
        portal_props = getToolByName(self, 'portal_properties')
        return portal_props.site_properties.getProperty('use_email_as_login')

    def _get_username_from_email(self, request, login_email):
        """Returns the username for a given email.

        If no user found it returns None.
        """
        matches = getBrainsForEmail(self, login_email, request=request)
        if len(matches) == 1:
            logger.debug("One match on email %s", login_email)
            return matches[0].getUserId
        elif len(matches) > 1:
            logger.warn("Multiple matches on email %s", login_email)
        else:
            logger.debug("No matches on email %s", login_email)

    # IExtractionPlugin implementation
    def extractCredentials(self, request):
        login_email = request.get("__ac_name", '').strip()

        if ((not self.site_policy_allows_email_login())
            or (login_email == '')
                or ('@' not in login_email)):
            return {}
        login_name = self._get_username_from_email(request, login_email)
        if login_name is not None:
            request.set("__ac_name", login_name)
            password = request.get("__ac_password", None)
            return {"login": login_name, "password": password}
        return {}


classImplements(RememberEmailAuth, interface.IRememberEmailAuth)

InitializeClass(RememberEmailAuth)
