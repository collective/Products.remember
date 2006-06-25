from Products.membrane.interfaces import IUserAuthProvider

class IRememberAuthProvider(IUserAuthProvider):
    """
    Marks remember auth providers so we can use a custom user id
    provider.
    """
