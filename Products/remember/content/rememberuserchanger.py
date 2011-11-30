from zope.interface import implements

# name of IMembraneUserChangerAvail interface has been changed
try:
    from Products.membrane.interfaces.user import IMembraneUserChangerAvail \
        as IMembraneUserChanger
    IMembraneUserChanger  # pyflakes
except:
    from Products.membrane.interfaces.user import IMembraneUserChanger

from Products.remember.interfaces import IRememberUserChanger


class RememberUserChanger(object):
    """
    adapter from IRememberUserChanger -> IMembraneUserChanger
    """

    implements(IMembraneUserChanger)

    def __init__(self, context):
        self.context = context

    def doChangeUser(self, login, password, **kwargs):
        """change the password for a given user"""
        # currently ignore the kwargs, but can be useful in the future
        IRememberUserChanger(self.context)._setPassword(password)

    def setPassword(self, password):
        """
        set the password on the remember member object
        """
        IRememberUserChanger(self.context)._setPassword(password)
