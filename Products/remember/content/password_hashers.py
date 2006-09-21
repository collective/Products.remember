import sha

from persistent.mapping import PersistentMapping
from zope.app.annotation.interfaces import IAnnotations
from zope.interface import implements

from Products.remember.config import ANNOT_KEY
from Products.remember.interfaces import IHashPW

class BCryptHash(object):
    """
    Adapts from IAnnotatable to IHashPW. Uses bcrypt to hash the password
    """
    implements(IHashPW)
    try:
        import bcrypt
    except ImportError:
        bcrypt = None

    def __init__(self, context):
        self.context = context
        if self.bcrypt is None:
            return
        annotations = IAnnotations(context)
        storage = annotations.setdefault(ANNOT_KEY,
                                         PersistentMapping())
        storage.setdefault('bcrypt_salt', self.bcrypt.gensalt())
        self.storage = storage
    
    def hashPassword(self, password):
        """
        Return a hashed version of password using bcrypt
        """
        return self.bcrypt.hashpw(password, self.storage['bcrypt_salt'])

    def isAvailable(self):
        return self.bcrypt is not None

class SHAHash(object):
    """
    Adapts from IAnnotatable to IHashPW. Uses SHA to hash the password
    """
    implements(IHashPW)

    def __init__(self, context):
        self.context = context
    
    def hashPassword(self, password):
        """
        Return a hashed version of password using SHA
        """
        return sha.new(password).hexdigest()
    
    def isAvailable(self):
        return True
