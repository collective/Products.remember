from zope.interface import Interface

from Products.Archetypes.interfaces import IReferenceable

from Products.membrane.interfaces import IUserAuthProvider
from Products.membrane.interfaces import IGroupsProvider
from Products.membrane.interfaces import IMembraneTool

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
    def isAvailable():
        """
        Returns if the specified encryption mechanism is supported
        """

    def hashPassword(password):
        """
        Returns a hashed version of the password
        """

    def validate(reference, attempt):
        """
        Returns True is attempt hashes to reference, False otherwise.
        """

class IRememberMembraneTool(IMembraneTool):
    """
    Create a new interface to allow configuration of remember on the membrane tool
    at setup time
    """

class IRememberUserChanger(IReferenceable):
    """
    IRemember user changer uses the _setPassword method
    This is the mutator function for the member object
    """
    def _setPassword(password):
        """
        Modify the password on the member object
        """
