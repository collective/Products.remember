from AccessControl import ClassSecurityInfo
from AccessControl.PermissionRole import rolesForPermissionOn
from Globals import InitializeClass

from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.Archetypes import public as atapi
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.membrane.interfaces import IUserAuthProvider
from Products.membrane.interfaces import IPropertiesProvider

from Products.remember.config import ALLOWED_MEMBER_ID_PATTERN
from Products.remember.config import DEFAULT_MEMBER_TYPE
from Products.remember.utils import stringToList
from Products.remember.utils import removeAutoRoles
from Products.remember.permissions import EDIT_PROPERTIES_PERMISSION
from Products.remember.permissions import VIEW_PUBLIC_PERMISSION

from member_schema import content_schema
metadata_schema = atapi.ExtensibleMetadata.schema.copy()

_marker = []

class BaseMember(object):
    """
    Abstract member object base class.
    """
    security = ClassSecurityInfo()

    implements(IUserAuthProvider, IPropertiesProvider)

    archetype_name = portal_type = meta_type = DEFAULT_MEMBER_TYPE
    base_archetype = None

    # Give a nice icon
    content_icon = "user.gif"
    
    # Note that we override BaseContent.schema
    schema = content_schema + metadata_schema
    
    global_allow = 0

    # for Plone compatibility -- managed by workflow state
    listed = 0

    default_roles = ('Member',)

    security.declarePrivate('getDefaultRoles')
    def getDefaultRoles(self):
        return self.default_roles

    security.declareProtected(VIEW_PUBLIC_PERMISSION, 'fileAs')
    def fileAs(self):
        """
        Returns a user friendly identifier of the member, fullname by
        default.  can be overridden in subclasses to support different
        filing policies.  Used by the title field.
        """
        return self.getFullname()

    #######################################################################
    # Validators and vocabulary methods
    #######################################################################
    security.declarePrivate('validate_id')
    def validate_id(self, id):
        # we can't always trust the id argument, b/c the autogen'd
        # id will be passed in if the reg form id field is blank
        form = self.REQUEST.form
        if form.has_key('id') and not form['id']:
            return self.translate('Input is required but no input given.',
                                  default='You did not enter a login name.'),
        elif self.id and id != self.id:
            # we only validate if we're changing the id
            mbtool = getToolByName(self, 'membrane_tool')
            if mbtool.getUserAuthProvider(id) is not None or \
                   not ALLOWED_MEMBER_ID_PATTERN.match(id) or \
                   id == 'Anonymous User':
                msg = "The login name you selected is already " + \
                      "in use or is not valid. Please choose another."
                return self.translate(msg, default=msg)

    security.declarePrivate('validate_password')
    def validate_password(self, password):
        # no change -- ignore
        if not password:
            return None
        regtool = getToolByName(self, 'portal_registration')
        return regtool.testPasswordValidity(password)

    security.declarePrivate('validate_roles')
    def validate_roles(self, roles):
        roles = stringToList(roles)
        valid = self.valid_roles()

        for r in roles:
            if r not in valid:
                return '%s is not a valid role.' % (r)
        return None

    security.declarePrivate('post_validate')
    def post_validate(self, REQUEST, errors):
        form = REQUEST.form
        if form.has_key('password'):
            password = form.get('password', None)
            confirm = form.get('confirm_password', None)

            if not password:
                errors['password'] = \
                    self.translate('Input is required but no input given.',
                                   default='You did not enter a password.')

            if not errors.get('password', None):
                if password and \
                       (password == REQUEST.get('id', None) or \
                        password == self.id):
                    errors['password'] = \
                        self.translate('id_pass_same',
                                       default="Your username and password are the " +
                                       "same.  This is really not a good idea.",
                                       domain='remember-plone'),
                    
            if not (errors.get('password', None)) and \
                   not (errors.get('confirm_password', None)):
                if password != confirm:
                    errors['password'] = \
                        errors['confirm_password'] = \
                        self.translate('Passwords do not match.',
                                       default='Passwords do not match.'),

    security.declarePublic('isValid')
    def isValid(self):
        """
        Check to make sure a Member object's fields satisfy schema
        constraints
        """
        errors = {}
        # make sure object has required data and metadata
        self.Schema().validate(self, None, errors, 1, 1)
        if errors:
            return 0
        return 1

    # Vocabulary methods
    def editors(self):
        ptool = getToolByName(self, 'portal_properties')
        return ptool.site_properties.available_editors

    def filtered_valid_roles(self):
        """ return valid roles minus any automatic roles """
        roles = list(self.valid_roles())
        removeAutoRoles(roles)
        return tuple(roles)

    def valid_groups(self):
        """ return the set of valid groups """
        gtool = getToolByName(self, 'portal_groups')
        return gtool.getGroupIds()

    def available_skins(self):
        # give managers the ability to choose any skin
        mtool = getToolByName(self, 'portal_membership')
        managePortal = mtool.checkPermission(CMFCorePermissions.ManagePortal,
                                             self)
        skins_tool = getToolByName(self, 'portal_skins')
        if skins_tool.getAllowAny() or managePortal:
            return getToolByName(self, 'portal_skins').getSkinSelections()
        else:
            return [self.getPortalSkin()]

    def getDefaultSkin(self):
        return getToolByName(self, 'portal_skins').getDefaultSkin()

    def getSiteLanguages(self):
        return atapi.DisplayList(self.availableLanguages())

    #######################################################################
    # Contract with portal_membership
    #######################################################################
    security.declarePublic('getMemberId')
    def getMemberId(self):
        """Get the member id """
        return self.getUserName()

    security.declareProtected(EDIT_PROPERTIES_PERMISSION, 'setProperties')
    def setProperties(self, mapping=None, **kwargs):
        """
        assign all the props to member attributes, we expect to be
        able to find a mutator for each of these props
        """
        # if mapping is not a dict, assume it is REQUEST
        if mapping:
            if not type(mapping) == type({}):
                data = {}
                for k,v in mapping.form.items():
                    data[k] = v
                mapping = data
        else:
            mapping = {}

        if kwargs:
            # mapping could be a request object thats not really a dict,
            # this is what we get
            mapping.update(kwargs)

        for fieldname in mapping.keys():
            # have to check permissions by hand... ugh!
            field = self.getField(fieldname)
            if field is not None and not field.checkPermission("edit", self):
                raise Unauthorized
                        
        self.update(**mapping)

    security.declarePrivate('setMemberProperties')
    def setMemberProperties(self, mapping):
        self.setProperties(mapping)

    def _getProperty(self, id):
        """Try to get a member property.  If the property is not found,
        raise an AttributeError"""
        field = self.Schema().get(id, None)
        if field is not None:
            if not field.checkPermission('view', self):
                raise Unauthorized
            accessor = getattr(self, field.accessor, None)
            value = accessor()
        else:
            base = aq_base(self)
            value = getattr(base, id)
        return value

    security.declarePublic('getProperty')
    def getProperty(self, id, default=_marker):
        try:
            return self._getProperty(id)
        except AttributeError:
            # member does not have a value for given property
            # try memberdata_tool for default value
            mdtool = getToolByName(self, 'portal_memberdata')
            tool_value = mdtool.getProperty(id, _marker)
            user_value = getattr(self.getUser(), id, _marker)

            # If the tool doesn't have the property, use user_value or default
            if tool_value is _marker:
                if user_value is not _marker:
                    return user_value
                elif default is not _marker:
                    return default
                else:
                    raise ValueError, 'The property %s does not exist' % id

            # If the tool has an empty property and we have a user_value, use it
            if not tool_value and user_value is not _marker:
                return user_value

            # Otherwise return the tool value
            return tool_value

    def isListed(self):
        # XXX this is rather inflexible...
        roles = rolesForPermissionOn('View', self)
        if 'Member' in roles:
            return 'Yes'
        else:
            return 'No'

    #######################################################################
    # IUserAuthProvider implementation
    #######################################################################
    def getUserName(self):
        return self.getId()

    def verifyCredentials(self, credentials):
        login = credentials.get('login')
        password = credentials.get('password')
        if login == self.getUserName() and password == self.getPassword():
            return True
        else:
            return False

InitializeClass(BaseMember)


class Member(BrowserDefaultMixin, BaseMember, atapi.BaseContent):
    """
    A regular non-folderish member content object.
    """
    security = ClassSecurityInfo()
    base_archetype = atapi.BaseContent

atapi.registerType(Member)
InitializeClass(Member)
