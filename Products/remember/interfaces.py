from zope.interface import Interface

from Products.membrane.interfaces import IUserAuthProvider
from Products.membrane.interfaces import IGroupsProvider

class IRememberAuthProvider(IUserAuthProvider):
    """
    Marks remember auth providers so we can use a custom user id
    provider.
    """

class IRememberGroupsProvider(IGroupsProvider):
    """
    Marks member objects as using the 'groups' field for groups
    instead of the default, which is references to group objects.
    """
    def getGroups(self):
        """
        Returns the groups this member belongs to.
        """

class IHashPW(Interface):
    """
    Hashes a password for member objects
    """
    def hashPassword(password):
        """
        Returns a hashed version of the password
        """
