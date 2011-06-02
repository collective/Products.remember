========
Products.remember
========

Products.remember is a full implementation of the default Plone member
configuration using content to represent membership accounts.  It is built
on top of Products.membrane.  Out of the box, Products.remember should work
very much like a regular Plone membership accounts, except that member
information is stored in Member objects that are (by default) stored in the
portal_memberdata tool.

This version works with versions of Plone 4.0 and later and
Products.membrane 2.0 and later.

Products.remember is a successor to CMFMember, which will not work with
PluggableAuthService-based user folders, and thus will not work with a
typical Plone 2.5 (and greater) installation.  Previous versions of
Products.remember, eg 1.1b3, provide a migration path for existing
CMFMember-based sites.

For questions and support, please see the Remember mailing list:
http://www.openplans.org/projects/remember/lists/remember/

============
INSTALLATION
============

Products.remember is packaged using Python's setuptools package management
infrastructure.  Remember can be made available to your Zope instance by
installing the Products.remember package into your Zope's python
environment, using either easy_install or 'python setup.py install'.

Products.remember is installed into a Plone site by the application of a
GenericSetup extension profile.  You can do this when creating a new
site by selecting remember from the list of available setup profiles
when you are creating the site.  In an existing site, you can use
Plone's regular product installation interface.

============
REQUIREMENTS
============

- Plone 4+
- membrane 2+

Optional:

- contentmigration (if migrating an existing CMFMember site)
  (http://svn.plone.org/svn/collective/contentmigration/trunk)

- py-bcrypt (http://www.mindrot.org/py-bcrypt.html or
             http://cheeseshop.python.org/pypi/bcrypt/0.1)
