import logging
from AccessControl import ClassSecurityInfo
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ManageUsers
from Products.PlonePAS.tools.membership import MembershipTool as BaseTool

logger = logging.getLogger('remember')

class MembershipTool(BaseTool):
    """
    remember customization of MembershipTool.
    """
    meta_type = "remember Membership Tool"
    
    security = ClassSecurityInfo()

    def _getMemberDataContainer(self):
        """
        Currently returns the portal_memberdata instance.  Soon will
        be replaced by a utility that determines where to put each new
        member object.
        """
        md_path = getattr(self, 'memberdata_container_path', None)
        if md_path is None:
            mdc = getToolByName(self, 'portal_memberdata')
            md_path = mdc.getPhysicalPath()
        return self.unrestrictedTraverse(md_path)

    def searchForMembers(self, REQUEST=None, **kw):
        """
        Here for backwards compatibility; ultimately delegates to the
        membrane_tool.
        """

        if type(REQUEST) == type({}):
            param = REQUEST # folder_localroles_form passes a dict here as REQUEST
            REQUEST = None
        elif REQUEST:
            param = REQUEST.form
        else:
            param = kw

        # mapping from older lookup names to the indexes that exist
        # in the membrane_tool
        key_map = {'name': 'getId',
                   'email': 'getEmail',
                   'roles': 'getRoles',
                   'groupname': 'getGroups', # XXX this is a case sensitive search, but is case insensitive in standard plone 2.1
                   'last_login_time': 'getLast_login_time',
                   }

        for key in key_map.keys():
            if param.has_key(key):
                # swap old parameter for what the catalog expects
                param[key_map[key]] = param.pop(key)
                
        return self._getMemberDataContainer().searchForMembers(REQUEST, **param)
