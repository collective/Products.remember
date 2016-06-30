Overview
========

Products.remember is a full implementation of the default Plone member
configuration using content to represent membership accounts.  It is built
on top of Products.membrane.  Out of the box, Products.remember should work
very much like a regular Plone membership accounts, except that member
information is stored in Member objects that are (by default) stored in the
portal_memberdata tool.

Products.remember 1.9+ works with Plone 4+ and Products.membrane 2+.  It
does not suppport Plone 3 and Products.membrane 1 - for that, see instead
versions of Products.remember before 1.9, eg 1.1b3.  Visit
https://pypi.python.org/pypi/Products.remember for the index of all
available Products.remember releases.

Products.remember is a successor to CMFMember, which will not work with
PluggableAuthService-based user folders, and thus will not work with a
contemporary Plone (2.5 and greater) installations.  Products.remember 1.1b3
provides a migration path for existing CMFMember-based sites.

For questions and support, please see the Remember mailing list:
http://www.coactivate.org/projects/remember/lists/remember


Release Notes - 1.9
===================

Tested with: Plone 4.2 and 4.3.

State: Final release

License: GPL

Release Manager: Ken Manheimer, Maurits van Rees

Compatible with/requires Plone 4.1+ and Products.membrane 2+.

Products.remember is now undisruptive when present but not installed, not
affecting operation of non-remember sites in the same instance.  Sites that
have Products.remember installed can now quick-uninstall to revert to plain
operation.  (The uninstall is not complete, however - see change log
notes.)

Products.remember membership now provides for email-address based logins
and respects "Use email address as login name" Site Setup / Security
setting.

Many internal changes for Plone 4 and Membrane 2 compatibility, JS
schemata/filedsets, and modernized GenericSetup and update configuration.


INSTALLATION
============

Products.remember is packaged using Python's setuptools package management
infrastructure.  Remember can be made available to your Zope instance by
installing the Products.remember package into your Zope's python
environment, using either buildout from pypi and/or using easy_install or
'python setup.py install'.

Products.remember is installed into a Plone site by the application of a
GenericSetup extension profile.  You can do this when creating a new
site by selecting remember from the list of available setup profiles
when you are creating the site.  In an existing site, you can use
Plone's regular product installation interface.


REQUIREMENTS
============

- Plone 4.1+
- Products.membrane 2+

Optional:

- py-bcrypt (http://code.google.com/p/py-bcrypt/ or
  https://pypi.python.org/pypi/py-bcrypt/)
