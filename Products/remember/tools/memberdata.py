from AccessControl import ClassSecurityInfo

from zope.interface import implements

from Products.CMFCore.interfaces import IMemberDataTool
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFCore import permissions as cmfcore_permissions
from Products.CMFCore.utils import getToolByName

from Products.PlonePAS.tools.memberdata import MemberDataTool \
     as BaseTool

from Products.Archetypes import public as atapi
from Products.remember.config import DEFAULT_MEMBER_TYPE

class MemberDataContainer(atapi.BaseBTreeFolder, BaseTool):
    """
    Default container for remember Member objects.  Members don't
    actually need to live here any more, but for BBB reasons we are
    still storing them here.
    """
    implements(IMemberDataTool)

    security = ClassSecurityInfo()

    id = 'portal_memberdata'
    archetype_name = meta_type = portal_type = 'MemberDataContainer'
    filter_content_types = 1
    allowed_content_types = [DEFAULT_MEMBER_TYPE]
    global_allow = 0
    content_icon = 'user.gif'

    manage_options = atapi.BaseBTreeFolder.manage_options + \
                     ActionProviderBase.manage_options

    def __init__(self, **kwargs):
        atapi.BaseBTreeFolder.__init__(self, self.id, **kwargs)
        BaseTool.__init__(self)

    ###################################################################
    # IMemberDataTool implemenation
    ###################################################################
    security.declarePrivate('wrapUser')
    def wrapUser(self, user):
        """
        If possible, returns the Member object that corresponds to the
        given User object.  Note that we're not actually wrapping the
        User object any longer, we're done w/ that mess.
        """
        mbtool = getToolByName(self, 'membrane_tool')
        mem = mbtool.getUserAuthProvider(user.getId())
        if mem is None:
            return BaseTool.wrapUser(self, user)

    security.declareProtected(cmfcore_permissions.ManageProperties,
                              'getMemberDataContents')
    def getMemberDataContents(self):
        """
        Returns a list containing a dictionary with information about
        the member objects: member_count is the total number of member
        instances stored in the memberdata- tool while orphan_count is
        the number of member instances that for one reason or another
        are no longer in the underlying acl_users user folder.

        NOTE: orphan_count will always be zero b/c it is now
        impossible to have orphaned member objects.  :-).
        """
        pass

    security.declareProtected(cmfcore_permissions.ManageProperties,
                              'pruneMemberDataContents')
    def pruneMemberDataContents(self):
        """
        Check for every Member object if it's orphan and delete it.

        The impl can override the pruneOrphan(id) method to do things
        like manage its workflow state. The default impl will remove.

        NOTE: This exists purely for BBB reasons; it does nothing, b/c
        it is now impossible to orphan member objects.
        """
        pass

    security.declarePrivate('searchMemberData')
    def searchMemberData(self, search_param, search_term, attributes=()):
        """ Search members. """
        pass

    security.declarePrivate('registerMemberData')
    def registerMemberData(self, m, id):
        """
        Add a member to the member set w/ the given member data.
        
        o 'm' is an object whose attributes are the memberdata for the
           member.

        o 'id' is the userid of the member.
        """
        pass

    security.declarePrivate('deleteMemberData')
    def deleteMemberData(self, member_id):
        """
        Delete member data of the specified member.
        """
        pass
