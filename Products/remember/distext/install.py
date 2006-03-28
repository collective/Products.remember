from distutils.command.install import install
from distutils.errors import DistutilsOptionError
from utils import useBuildPath, getBuildPath
import os, sys



PRODUCT_SCHEME = {
    'purelib': '$base',
    'platlib': '$base',
    'data'   : '$base',
    }

SCHEME_KEYS = ('purelib', 'platlib', 'data')


class InstallCommand(install):
    """Build and install a Product in a Zope/Plone site"""

    description = """Build and install a Product in a Zope/Plone site"""

    def finalize_options(self):
        if not self.prefix or not os.access(self.prefix, os.W_OK):
            self.guess_prefix()

        install.finalize_options(self)
        # Process the install arguments as they exist in stock
        # distutils to mean a Products directory

        if not self.prefix:
            raise DistutilsOptionError, \
                  ("must supply a prefix that is your products directory")
        if not os.access(self.prefix, os.W_OK):
            raise DistutilsOptionError, \
                  ("specify your products dir using --prefix (must be writeable)")

    def guess_prefix(self):
        """The user could have set an environ var for Products"""
        # XXX: or set a file in their homedir
        pd = os.environ.get("PRODUCTS_DIR")
        if pd is not None:
            self.prefix = pd

    def select_scheme(self, name):
        """Ignore the scheme the system detected and use the uniform
        product installer (which is flat)
        """
        # it's the caller's problem if they supply a bad name!
        scheme = PRODUCT_SCHEME
        for key in SCHEME_KEYS:
            attrname = 'install_' + key
            setattr(self, attrname, scheme[key])
