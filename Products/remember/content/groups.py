from AccessControl import ClassSecurityInfo
from Products.membrane.factories.groups import Groups as BaseGroups

class Groups(BaseGroups):
    """
    Adapts from IRememberGroupsProvider to IMembraneUserGroups.
    Overrides the default membrane plug-in which uses content for
    groups, instead just uses the value of the 'groups' field on the
    member object.
    """
    security = ClassSecurityInfo()
    
    security.declarePrivate('getGroupsForPrincipal')
    def getGroupsForPrincipal(self, principal, request=None):
        return self.context.getGroups()
