
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
WARNING!!:  ALWAYS PERFORM THIS MIGRATION (and all migrations) ON A
TEST DEPLOYMENT BEFORE TRYING IT ON YOUR LIVE DATA, AND TEST
THOROUGHLY BEFORE COMMITTING TO THE PROCESS.  AND ALWAYS HAVE A BACKUP
THAT YOU CAN SAFELY REVERT TO IF SOMETHING GOES WRONG.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Thanks to Ross Patterson for providing the initial CMFMember->remember
migration code, which was integrated into remember (with significant
modifications) by Rob Miller.

This package contains code required to do a migration from a Plone
2.1.x site running CMFMember to a Plone 2.5.x site running remember.
The process for performing a migration is as follows:

- Shut down the running 2.1.x site.

- Upgrade all of the underlying Plone software to what is required for
  Plone 2.5.x, and add the membrane and remember products to your
  Products directory.  Do NOT remove the CMFMember product.
  (Alternatively, you can copy your ZODB from the 2.1.x installation
  to another deployment running the 2.5.x stack w/ remember and
  membrane.  You WILL need to have CMFMember installed in the 2.5.x
  deployment.)

- Install the 'contentmigration' product into the Plone 2.5.x Zope
  instance.
  (http://svn.plone.org/svn/collective/contentmigration/trunk)

- Edit remember's config.py file so that CMFMEMBER_MIGRATION_SUPPORT
  is set to True

- Start the 2.5.x Zope instance.

- Visit the portal_migration tool and run the Plone migration process,
  just as you would normally.

- Finally, when you're satisfied everything is working correctly, you
  can use the 'remove_cmfmember' External Method to remove the traces
  of CMFMember from your site.  Once you've done this, you can remove
  the CMFMember product from your Zope instance entirely.

That should be it; if you've activated the
CMFMEMBER_MIGRATION_SUPPORT, then the portal migration process should
also engage the CMFMember->remember migration process, and you should
be pretty close to ready.  There are a number of gotchas to be aware
of, however:

- Workflows:

  By default, this migration will delete the CMFMember workflows and
  will replace them with very similar remember implementations of the
  same workflows.  All of the member objects associated with these
  workflows should end up in the same state as they were in before the
  migration.  IF YOU HAVE MADE ANY CUSTOMIZATIONS TO THE CMFMEMBER
  DEFAULT WORKFLOWS, THESE WILL BE LOST!  If you have made such
  customizations and you want to avoid losing them, you can visit the
  remember/cmfmember/config.py file and change the
  REPLACE_CMFMEMBER_WORKFLOWS setting to False.  You will then be
  responsible for tweaking your custom workflows to work correctly in
  the remember environment.

- Custom member types:

  This migration seems to work reasonably well for converting the
  default CMFMember member objects into default remember member
  objects.  It also attempts to provide a means to help you migrate
  custom member types as well.  THIS MAY OR MAY NOT WORK, PLEASE TEST
  VERY THOROUGHLY BEFORE TRUSTING THIS!  If you're interested in
  trying this out, the following guidelines should help.

  You'll need to implement a new class for your remember-based member
  objects; the CMFMember base classes will no longer be suitable, you
  should use the base classes that remember provides.  Usually you can
  use the same schema without modifications.  It is recommended that
  you use the same meta_type and portal_type for your new member type
  that you used for the old one.

  Before you run the migration, you'll want to edit the MIGRATION_MAP
  data structure in remember/cmfmember/config.py.  The key for your
  entry should be the class of your new member type, and the value
  should be a dictionary that contains info used by the migration
  process.  Please see that file to see the exact structure this
  should take.
  
  If you have custom workflows, you may decide to make some slight
  changes in these as you migrate to remember.  The migration supports
  removing the existing workflows and replacing them with the new
  implementations.  It is very important that you use the same
  workflow ID, however, or else the state information for all of your
  existing member objects will be lost.
