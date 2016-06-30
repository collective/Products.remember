import hashlib
import hmac

from persistent.mapping import PersistentMapping
from zope.annotation.interfaces import IAnnotations
from zope.interface import implements

from AccessControl.AuthEncoding import pw_encrypt
from AccessControl.AuthEncoding import pw_validate

from Products.remember.config import ANNOT_KEY
from Products.remember.interfaces import IHashPW


class BaseHash(object):
    """
    Abstract base class for actual hashing implementations.
    """
    implements(IHashPW)

    def __init__(self, context):
        self.context = context

    def isAvailable(self):
        return True

    def hashPassword(self, password):
        raise NotImplementedError

    def validate(self, reference, attempt):
        """
        Check to see if the reference is a hash of the attempt.
        """
        return self.hashPassword(attempt) == reference


class BCryptHash(BaseHash):
    """
    Adapts from IAnnotatable to IHashPW. Uses bcrypt to hash the
    password
    """
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

    def isAvailable(self):
        return self.bcrypt is not None

    def hashPassword(self, password):
        """
        Return a hashed version of password using bcrypt
        """
        return self.bcrypt.hashpw(password, self.storage['bcrypt_salt'])


class SHAHash(BaseHash):
    """
    Adapts from IAnnotatable to IHashPW. Uses SHA to hash the password
    """

    def hashPassword(self, password):
        """
        Return a hashed version of password using SHA
        """
        return hashlib.sha1(password).hexdigest()


class HMACHash(BaseHash):
    """
    Adapts from IAnnotatable to IHashPW. Uses SHA to hash the password
    """

    def __init__(self, context):
        self.context = context
        key = str(context)
        annotations = IAnnotations(context)
        storage = annotations.setdefault(ANNOT_KEY,
                                         PersistentMapping())
        storage.setdefault('hmac_key', key)
        self.storage = storage

    def hashPassword(self, password):
        """
        Return a hashed version of password using SHA
        """
        return hmac.new(self.storage['hmac_key'], password, hashlib.sha1
                        ).hexdigest()


class ZAuthHash(BaseHash):
    """
    Adapts from IAnnotatable to IHashPW. Uses Zope 2's
    AccessControl.AuthEncoding module to hash the password.
    """

    def hashPassword(self, password):
        """
        Delegate to AccessControl.AuthEncoding.
        """
        return pw_encrypt(password)

    def validate(self, reference, attempt):
        """
        Check to see if the reference is a hash of the attempt.
        """
        return pw_validate(reference, attempt)
