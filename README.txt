========
Remember
========

Remember is a full implementation of the default Plone member
configuration using content to represent the members, built on top of
Membrane.  Out of the box, Remember should work very much like a
regular Plone site, except that member information is stored in Member
objects that are (by default) stored in the portal_memberdata tool.

Remember is a successor to CMFMember, which will not work with
PluggableAuthService-based user folders, and thus will not work with a
typical Plone 2.5 (and greater) installation.

See Products.remember releases prior to version 1.9 for migration from
existing CMFMember-based sites.

NOTE: This version of Remember requires Plone 4 and membrane 2.

For questions and support, please see the Remember mailing list:
http://www.openplans.org/projects/remember/lists/remember/

============
INSTALLATION
============

Remember is packaged using Python's setuptools package management
infrastructure.  Remember can be made available to your Zope instance
by installing the Products.remember package into your Zope's python
environment, using either easy_install or 'python setup.py install'.

Remember is installed into a Plone site by the application of a
GenericSetup extension profile.  You can do this when creating a new
site by selecting remember from the list of available setup profiles
when you are creating the site.  In an existing site, you can use
Plone's regular product installation interface.

============
REQUIREMENTS
============

- Zope 2.12.X
- Plone 4+
- membrane 2+

Optional:

- py-bcrypt (http://www.mindrot.org/py-bcrypt.html or 
             http://cheeseshop.python.org/pypi/bcrypt/0.1)
