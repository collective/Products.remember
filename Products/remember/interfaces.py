from Products.membrane.interfaces import IUserAuthentication

class IRememberAuthentication(IUserAuthentication):
    """
    Marks remember auth providers so we can use a custom user id
    provider.
    """
