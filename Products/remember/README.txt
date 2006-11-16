remember

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
