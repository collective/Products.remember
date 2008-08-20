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
typical Plone 2.5 (and greater) installation.  There is a migration
path provided for folks with existing CMFMember-based sites who would
like to migration to Plone 2.5.X and Remember.  For instructions on
performing such migrations, please refer to the README.txt file in
the cmfmember subdirectory.

NOTE: This version of Remember requires Plone 3.0 or 3.1, it does NOT
support Plone 2.5.  If you have a CMFMember-based Plone 2.1 solution,
you should initially migrate to Remember 1.0 and Plone 2.5.  Once this
is working correctly, then you can upgrade to Remember 1.1 and Plone 3
with little problem.

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

- Zope 2.10.X
- Plone 3.0.X or 3.1.X
- membrane 1.1

Optional:

- contentmigration (if migrating an existing CMFMember site)
  (http://svn.plone.org/svn/collective/contentmigration/trunk)

- py-bcrypt (http://www.mindrot.org/py-bcrypt.html or 
             http://cheeseshop.python.org/pypi/bcrypt/0.1)
