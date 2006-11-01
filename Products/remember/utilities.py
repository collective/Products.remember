from zope.interface import implements

from OFS.SimpleItem import SimpleItem

from Products.CMFCore.utils import getToolByName

from Products.membrane.interfaces import IUserAdder
from Products.remember.config import DEFAULT_MEMBER_TYPE

class UserAdder(SimpleItem):
    """
    UserAdder that adds the current default remember-based member
    types.
    """
    implements(IUserAdder)

    # can be changed by the configlet
    default_member_type = DEFAULT_MEMBER_TYPE

    def addUser(self, login, password):
        """
        Adds the appropriate type of remember object in
        portal_memberdata.
        """
        mdtool = getToolByName(self, 'portal_memberdata')
        mtype = self.default_member_type
        mdtool.invokeFactory(mtype, login, password=password)
