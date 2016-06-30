import logging
from AccessControl import Unauthorized
from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin

logger = logging.getLogger('Products.remember.pas.utils')


def getBrainsForEmail(context, email, request=None):
    """Anonymous users should be able to look for email addresses.
    Otherwise they cannot log in.

    This searches in the membrane_tool and returns brains with this
    email address.  Hopefully the result is one or zero matches.
    """
    try:
        email = email.strip()
    except ValueError:
        return []
    if email == '' or '@' not in email:
        return []
    if request is None:
        try:
            request = context.REQUEST
        except:
            # Happens e.g. when submitting a change in the
            # prefs_user_overview.  Just use None.
            pass
    user_catalog = getToolByName(context, 'membrane_tool', None)
    if user_catalog is None:
        logger.warn("membrane_tool not found.")
        return []

    kw = dict(getEmail=email)

    # this was using search(), but need to switch to Catalog.searchResults()
    # because incompatibility with CatalogSearchArgumentsMap and hotfix
    # 20131210
    users = user_catalog.unrestrictedSearchResults(request, **kw)

    # Searching for joe@example.org also returns john-joe@example.org.
    # But here we only want exact matches.
    exact = [user for user in users if user.getEmail == email]
    return exact


def getUserIdForEmail(context, email):
    brains = getBrainsForEmail(context, email)
    if len(brains) == 1:
        return brains[0].getUserId
    return ''


def validate_unique_email(context, email):
    """Validate this email as unique in the site.
    """
    matches = getBrainsForEmail(context, email)
    if not matches:
        # This email is not used yet.  Fine.
        return
    if len(matches) > 1:
        msg = "Multiple matches on email %s" % email
        logger.warn(msg)
        return msg
    # Might be this member, being edited.
    match = matches[0]
    try:
        found = match.getObject()
    except (AttributeError, KeyError, Unauthorized):
        # This is suspicious.  Best not to use this one.
        pass
    else:
        if found == context:
            # We are the only match.  Good.
            logger.debug("Only this object itself has email %s", email)
            return

    # There is a match but it is not this member or we cannot get
    # the object.
    msg = "Email %s is already in use." % email
    logger.debug(msg)
    return msg


def email_login_is_active():
    context = getSite()
    portal_props = getToolByName(context, 'portal_properties')
    if not portal_props.site_properties.getProperty('use_email_as_login'):
        return False
    acl = getToolByName(context, 'acl_users')
    # Import here to avoid circular import:
    from Products.remember.pas.plugin import RememberEmailAuth
    plugins = acl.plugins.listPlugins(IExtractionPlugin)
    for plugin_id, plugin in plugins:
        if plugin.__class__ == RememberEmailAuth:
            return True
