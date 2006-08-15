import logging
from AccessControl import ClassSecurityInfo
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

    security.declarePrivate('addMember')
    def addMember(self, id, password, roles, domains, properties=None):
        """
        Adds a new member to the user folder.  Security checks will
        have already been performed.  Called by portal_registration.
        """
        mdc = self._getMemberDataContainer()
        member_type = mdc.getDefaultType()
        mdc.invokeFactory(member_type, id)
        member = mdc._getOb(id)
        logger.info('\n\n the props be:\n\n' + str(properties))
        member.edit(password=password, roles=roles,
                    domains=domains, **(properties or {}))
    
    security.declareProtected(ManageUsers, 'deleteMembers')
    def deleteMembers(self, members, delete_memberareas=1,
                      delete_localroles=1):
        """Delete members specified by member_ids.
        """
        # Delete the member objects
        dels = {}
        mbtool = getToolByName(self, 'membrane_tool')
        membrains = mbtool(getId=members)
        for brain in membrains:
            if dels.has_key(brain.parent_path):
                dels[brain.parent_path].append(brain.getId)
            else:
                dels[brain.parent_path] = [brain.getId]
        for parent_path, del_ids in dels.items():
            parent = self.unrestrictedTraverse(parent_path)
            parent.manage_delObjects(del_ids)

        mem_ids = [b.getId for b in membrains]
        # Delete members' home folders including all content items.
        if delete_memberareas:
            for mem_id in mem_ids:
                 self.deleteMemberArea(mem_id)

        # Delete members' local roles.
        if delete_localroles:
            utool = getToolByName(self, 'portal_url', None)
            self.deleteLocalRoles( utool.getPortalObject(), mem_ids,
                                   reindex=1, recursive=1 )

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
                   'roles': 'getFilteredRoles',
                   'groupname': 'getGroups', # XXX this is a case sensitive search, but is case insensitive in standard plone 2.1
                   'last_login_time': 'getLastLoginTime',
                   }
        for key in key_map.keys():
            if param.has_key(key):
                # swap old parameter for what the catalog expects
                param[key_map[key]] = param.pop(key)
                
        return self._getMemberDataContainer().searchForMembers(REQUEST, **param)
