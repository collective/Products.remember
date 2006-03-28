"""
pkgconfig
~~~~~~~~~~~~~~~~~~~~
A small wrapper around pkg-config program used to manage libraries and
dependencies.

"""

__author__ = 'Benjamin Saller <bcsaller@objectrealms.net>'
__docformat__ = 'restructuredtext'
__copyright__ = 'Copyright ObjectRealms, LLC. 2005'
__license__  = 'The GNU Public License V2+'


from subprocess import Popen, PIPE

PKG_CONFIG="pkg-config"
def pkgconfig(packages):
    """Given a list of packages return a list of all includes and a
    list of all library dependencies. If the package doesn't exist and
    exception will be thrown
    """

    # Process Includes
    includes = "%s --cflags-only-I %s" % (PKG_CONFIG, packages)
    p = Popen([includes], shell=True,
              stdin=PIPE, stdout=PIPE, stderr=PIPE,
              close_fds=True)

    includes_list = [b[2:] for b in p.stdout.read().split()]
    p.wait()
    if p.returncode != 0: raise ValueError(p.stderr.read())

    # Process Libs
    libs = "%s --libs-only-l %s" % (PKG_CONFIG, packages)
    p = Popen([libs], shell=True,
              stdin=PIPE, stdout=PIPE, stderr=PIPE,
              close_fds=True)

    libs_list = [b[2:] for b in p.stdout.read().split()]
    p.wait()
    if p.returncode != 0: raise ValueError(p.stderr.read())

    return includes_list, libs_list
