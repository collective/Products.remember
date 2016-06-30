from sets import Set

from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass

from zope.interface import implements

from Products.CMFCore.interfaces import IMemberDataTool
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFCore import permissions as cmfcore_permissions
from Products.CMFCore.utils import getToolByName

from Products.PlonePAS.tools.memberdata import MemberDataTool \
    as BaseTool

from Products.Archetypes import public as atapi
from Products.remember.config import DEFAULT_MEMBER_TYPE
from Products.remember.interfaces import IMemberDataContainer

schema = atapi.BaseFolderSchema.copy() + atapi.Schema((

    # use MetadataStorage so as not to conflict w/ the 'description'
    # property used for old-school MemberData objects
    atapi.TextField(
        'description',
        default='Container for Members',
        widget=atapi.TextAreaWidget(rows=5),
        storage=atapi.MetadataStorage(),
    ),
))

search_catalog = 'membrane_tool'


class MemberDataContainer(atapi.BaseBTreeFolder, BaseTool):
    """
    Default container for remember Member objects.  Members don't
    actually need to live here any more, but for BBB reasons we are
    still storing them here.
    """
    implements(IMemberDataTool, IMemberDataContainer)

    security = ClassSecurityInfo()

    id = 'portal_memberdata'
    archetype_name = meta_type = portal_type = 'MemberDataContainer'
    filter_content_types = 1
    allowed_content_types = [DEFAULT_MEMBER_TYPE]
    global_allow = 0
    content_icon = 'user.gif'
    schema = schema
    _description = None

    manage_options = atapi.BaseBTreeFolder.manage_options + \
        ActionProviderBase.manage_options

    def __init__(self, **kwargs):
        atapi.BaseBTreeFolder.__init__(self, self.id, **kwargs)
        BaseTool.__init__(self)
        self.title = 'Member Profiles'

    ###################################################################
    # Property hack to mask the unused 'description' attribute
    # inherited from PortalFolderBase
    ###################################################################
    def _getDescription(self):
        """
        Masks the 'description' attribute that is inherited from the
        PortalFolderBase class.
        """
        if getattr(self.aq_base, '_description') is None:
            raise AttributeError
        else:
            return self._description

    def _setDescription(self, desc):
        """
        Storing the description makes the property getter behave
        differently.
        """
        self._description = desc

    description = property(fget=_getDescription,
                           fset=_setDescription)

    ###################################################################
    # IMemberDataTool implementation
    ###################################################################
    def wrapUser(self, user):
        """
        If possible, returns the Member object that corresponds to the
        given User object.
        """
        mbtool = getToolByName(self, 'membrane_tool')
        mem = mbtool.getUserObject(user.getUserName())
        if mem is None:
            return BaseTool.wrapUser(self, user)
        return mem.__of__(self).__of__(user)
    security.declarePrivate('wrapUser')

    def getMemberDataContents(self):
        """
        Returns a list containing a dictionary with information about
        the member objects: member_count is the total number of member
        instances stored in the memberdata tool while orphan_count is
        the number of member instances that for one reason or another
        are no longer in the underlying acl_users user folder.

        NOTE: orphan_count will always be zero b/c it is now
        impossible to have orphaned member objects.  :-).
        """
        pass
    security.declareProtected(cmfcore_permissions.ManageProperties,
                              'getMemberDataContents')

    def pruneMemberDataContents(self):
        """
        Check for every Member object if it's orphan and delete it.

        The impl can override the pruneOrphan(id) method to do things
        like manage its workflow state. The default impl will remove.

        NOTE: This exists purely for BBB reasons; it does nothing, b/c
        it is now impossible to orphan member objects.
        """
        pass
    security.declareProtected(cmfcore_permissions.ManageProperties,
                              'pruneMemberDataContents')

    def searchMemberData(self, search_param, search_term, attributes=()):
        """ Search members. """
        pass
    security.declarePrivate('searchMemberData')

    def registerMemberData(self, m, id):
        """
        Add a member to the member set w/ the given member data.

        o 'm' is an object whose attributes are the memberdata for the
           member.

        o 'id' is the userid of the member.
        """
        pass
    security.declarePrivate('registerMemberData')

    def deleteMemberData(self, member_id):
        """
        Delete member data of the specified member.
        """
        pass
    security.declarePrivate('deleteMemberData')

    def getNotAddableTypes(self):
        """
        Only allow managers to add members
        """
        from Products.CMFCore.utils import _getAuthenticatedUser
        user = _getAuthenticatedUser(self)

        if 'Manager' in user.getRoles():
            return ()
        else:
            return self.getAllowedMemberTypes()

    def getAllowedMemberTypes(self):
        """
        Return the allow types from the membrane tool
        """
        mbtool = getToolByName(self, 'membrane_tool')
        return mbtool.listMembraneTypes()

    def searchForMembers(self, REQUEST=None, **kw):
        """
        Do a catalog search on a sites members. If a 'brains' argument
        is set to a True value, search will return only member_catalog
        metadata.  Otherwise, full member objects are returned.

        If 'brains' is a False value and a 'portal_only' parameter is
        passed in with a True value then only members from the
        portal's acl_users folder will be returned.
        """
        if REQUEST:
            search_dict = getattr(REQUEST, 'form', REQUEST)
        else:
            REQUEST = {}
            search_dict = kw

        results = []
        catalog = getToolByName(self, search_catalog)

        # only iterate over the indexes we're searching on
        indexes = Set(catalog.indexes())
        indexes = indexes & Set(search_dict.keys())

        query = {}

        def dateindex_query(field_value, field_usage):
            usage, val = field_usage.split(':')
            return {'query': field_value, usage: val}

        def zctextindex_query(field_value):
            # Auto Globbing
            if not field_value.endswith('*') and field_value.find(' ') == -1:
                field_value += '*'
            return field_value

        special_query = dict((
            ('DateIndex', dateindex_query),
            ('ZCTextIndex', zctextindex_query)
        ))

        if search_dict:
            # Make a indexname: fxToApply dict
            idx_fx = dict(
                [(x.id, special_query[x.meta_type])
                 for x in catalog.Indexes.objectValues()
                 if (x.meta_type in special_query.keys() and x.id in indexes)]
            )

            for i in indexes:
                val = search_dict.get(i, None)
                usage_val = search_dict.get('%s_usage' % i)
                if type(val) == type([]):
                    val = filter(None, val)

                if (i in idx_fx.keys() and val):
                    if usage_val:
                        val = idx_fx[i](val, usage_val)
                    else:
                        val = idx_fx[i](val)

                if val:
                    query.update({i: val})

        results = catalog(query)

        # return objects by default
        if results and not (search_dict.get('brains', False) or
                            REQUEST.get('brains', False)):
            if search_dict.get('portal_only', False) or \
                    REQUEST.get('portal_only', False):
                res = []
                for r in results:
                    mem = r.getObject()
                    if mem._isPortalUser():
                        res.append(mem)
                results = res
            else:
                results = [r.getObject() for r in results]

        return filter(None, results)

    def _getPortrait(self, member_id):
        uf = getToolByName(self, 'acl_users')
        user = uf.getUserById(member_id)
        if user is None:
            return BaseTool._getPortrait(self, member_id)
        portrait = user.getProperty('portrait', None)
        if portrait is None:
            return BaseTool._getPortrait(self, member_id)
        return portrait

atapi.registerType(MemberDataContainer, 'remember')
InitializeClass(MemberDataContainer)
