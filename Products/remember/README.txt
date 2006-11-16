========
remember
========

remember is a full implementation of the default Plone member
configuration using content to represent the members, built on top of
membrane.  Out of the box, remember should work very much like a
regular Plone site, except that member information is stored in Member
objects that are (by default) stored in the portal_memberdata tool.

remember is a successor to CMFMember, which will not work with
PluggableAuthService-based user folders, and thus will not work with a
typical Plone 2.5 (and greater) installation.  There is a migration
path provided for folks with existing CMFMember-based sites who would
like to migration to Plone 2.5.2 and remember.  For instructions on
performing such migrations, please refer to the README.txt file in
the cmfmember subdirectory.

For questions and support, please see the remember mailing list:
http://www.openplans.org/projects/remember/lists/remember/

============
INSTALLATION
============

To install remember into your Zope instance, put the remember code in
a directory named "remember" in your instance home's Products
directory and restart Zope.

remember is installed into a Plone site by the application of a
GenericSetup extension profile.  You can do this when creating a new
site by selecting both membrane and remember from the list of
available setup profiles when you are creating the site.  In an
existing site, you install an extension profile using the ZMI of the
portal_setup tool.  First browse to the properties tab and specify the
profile in question as the "active" profile.  Then browse to the
import tab and click on the "Run all import steps" button near the
bottom of the page.  You will want to perform these steps first for
the membrane profile, then for the remember profile.

NOTE: While remember does provide a migration path for existing, Plone
2.1-based CMFMember sites, it does NOT yet provide a way to migrate
existing default Plone members to remember-based members.  This is
intended to be in place before the final 1.0 release.

============
REQUIREMENTS
============

- Zope 2.9.5 (or greater)
- Plone 2.5.2 (unreleased, please use 2.5-zope29 bundle until 2.5.2 is
               officially released)
- Five 1.4.1
- membrane 1.0b1 (or greater)

Optional:

- contentmigration (if migrating an existing CMFMember site)
  (http://svn.plone.org/svn/collective/contentmigration/trunk)

- py-bcrypt (http://www.mindrot.org/py-bcrypt.html or 
             http://cheeseshop.python.org/pypi/bcrypt/0.1)
