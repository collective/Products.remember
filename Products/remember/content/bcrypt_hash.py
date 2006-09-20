import bcrypt

from persistent.mapping import PersistentMapping
from zope.app.annotation.interfaces import IAnnotations
from zope.interface import implements

from Products.membrane.interfaces import IUserRelated

class BCryptHash(object):
    """
    Adapts from IUserAuthProvider to IHashPW. Uses bcrypt to has the password
    """
    implements(IUserRelated)

    def __init__(self, context, annotatable):
        self.context = context
        annotations = IAnnotations(annotatable)
        storage = annotations.setdefault('Products.remember',
                                         PersistentMapping())
        storage.setdefault('bcrypt_salt', bcrypt.gensalt())
        self.storage = storage
    
    def hashPassword(self, password):
        """
        Return a hashed version of password using bcrypt
        """
        return bcrypt.hashpw(password, self.storage['bcrypt_salt'])
