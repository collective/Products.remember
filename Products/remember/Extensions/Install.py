from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin

from Products.remember import config
from Products.remember.content.member import Member
from Products.remember.permissions import SITEWIDE_PERMISSIONS

def setSitewidePermissions(portal, out):
    """Set site-wide security settings"""
    for roles, perms in SITEWIDE_PERMISSIONS:
        for perm in perms:
            print >> out, '-> Give roles %s permission "%s"' % (str(roles), perm)
            portal.manage_permission(perm, roles=roles)


def setMembraneTypes(self, out):
    """
    Specify the default membrane types.
    """
    mbtool = getToolByName(self, 'membrane_tool')
    mbtool.registerMembraneType(Member.portal_type)

def install(self):
    out = StringIO()

    install_subskin(self, out, config.GLOBALS)
    installTypes(self, out, listTypes(config.PROJECT_NAME),
                 config.PROJECT_NAME)
    setSitewidePermissions(self, out)
    setMembraneTypes(self, out)

    print >> out, "Successfully installed %s." % config.PROJECT_NAME
    return out.getvalue()
