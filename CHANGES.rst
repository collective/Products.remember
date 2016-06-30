Changelog
=========

1.9.4 (2016-06-30)
------------------

- Added Products.PloneTestCase to test requirements.  [maurits]

- Replace deprecated gif-icons with png-icons.
  This fixes https://github.com/collective/Products.remember/issues/10
  [WouterVH]


1.9.3 (2013-12-30)
------------------

- Password reset did not work with Hotfix 2013-12-10.
  Fixes issue https://github.com/collective/Products.remember/issues/6
  [miohtama]

- mailPassword needs to accept immediate parameter
  Fixes issue https://github.com/collective/Products.remember/issues/5
  [vangheem]


1.9.2 (2013-03-31)
------------------

- Setting the user email through the users and groups control panel no
  longer destroys the password.
  Fixes https://github.com/collective/Products.remember/issues/3
  [maurits]

- Made compatible with Plone 4.3.  Lost compatibility with Plone 4.0.
  [maurits]

- Removed deprecated prefs_users_overview.cpt plus metadata.  This is
  not used anymore in standard Plone.  Our metadata gave a form
  controller error and if we fixed that then the template would need
  to be fixed too.
  Fixes https://github.com/collective/Products.remember/issues/1
  [maurits]


1.9.1 (2011-12-16)
------------------

- Added upgrade step to restore our portal_memberdata settings, as
  they get destroyed by an upgrade to Plone 4.
  [maurits]


1.9 (2011-12-01)
----------------

- Protect the password field of members so the hash can not be seen.
  [maurits]

- Fixed tests and uninstall.
  [maurits]

- Fix usergroups_usersoverview.pt view to open correctly instead of crashing
  when you have member types without proper
  portal_type info available. This can be a case e.g. with abstract types.
  [miohtama]

1.9b1 - 2011-06-14
------------------

- Products.remember now can be installed in a portal without affecting
  the operation of the other portals in the same Zope instance.
  [may 2011 ken manheimer]

- Products.remember no longer disrupts non-membrane membership when
  Products.remember is present but not yet quick-installed.
  [march 2011 ken manheimer]

- Products.remember can now be quick-uninstalled, so that plain members can
  be created and operate properly.  The uninstall is not complete, however!
  The portal still depends on presence of the Products.remember code for
  proper operation, even when the product is not quick-installed.

  If Products.remember is subsequently re-installed, already-existing
  Products.remember accounts will resume working.  (You have to manually
  reindex the membrane_tool catalog to see the pre-existing accounts after
  reinstall.  Via the ZMI in your site's membrane_tool, select the
  'Advanced' tab and 'Update Catalog'.)

  Note that, as of this writing, Products.membrane cannot be uninstalled
  without breaking the site - but that should not interfere with operation
  or creation of plain, non-membrane membership accounts.
  [may 2011 ken manheimer]

- Respect Site Setup/Security/"Use email address as login name".

  New accounts are not allowed to have the same email address as already
  existing ones when the "Use email address as login name" property is
  True, but the policy is not enforced when it is false.  (Already existing
  accounts are not subject to the constraint in either case.)

  This feature is essentially Maurits van Rees' maurits-emaillogin-pas
  email login branch, plus: added automatic activation of the PAS
  authentication plugin, connection so it's controlled by the security
  setup "Use email address as login name" setting, and update step so the
  plugin is activated when portals already using Products.remember are
  upgraded.
  [march 2011 ken manheimer]

- Products.remember now depends on Products.membrane 2+ and Plone 4+:

  - Removed and/or converted "I*Avail" interfaces
  - Added missing BaseMember.getUserId() method
  - Make BaseMember Provide IMembraneUserAuth, so it can do
    .authenticateCredentials(), and
  - Implemented BaseMember.authenticateCredentials() method to be
    used instead of the version removed from membrane.

  NOTE WELL:

  If you have sites with pre-existing member objects you must update their
  membrane_tool catalog when you upgrade.  Via the ZMI in your site's
  membrane_tool, select the 'Advanced' tab and 'Update Catalog' to
  reconcile existing index entries.
  [march 2011 ken manheimer]

- Modernized GenericSetup configuration, moving the profile and import
  step registration from python code and xml to zcml, and creating
  upgrade steps to get rid of persistent import steps and update the
  existing getRoles index from a FieldIndex to a KeywordIndex.
  [maurits]

- Changed getRoles from a FieldIndex to a KeywordIndex in the
  membrane_tool, so you can search for roles.
  [maurits]

- Use Plone 3's JS schemata/fieldset switching.
  http://plone.org/products/remember/issues/55 [Matthew Wilkes]


1.1b3 - 2009-03-23
------------------

- allow usage of portal_registration tools  ALLOWED_MEMBER_ID_PATTERN. This
  does not change any current behaviour, it may be made configurable ttw in
  future. Introduced new config.py variable USE_PORTAL_REGISTRATION_PATTERN
  set to False by default. Setting to True switches to portal_registrations
  getIDPattern.
  [2009-04-23 by jensens]

- Fix inefficiency in prefs_users_overview where searchUsers is called when
  no search string is supplied. The bug meant that the page would be extremely
  slow even when just navigating to prefs_users_overview.
  [2009-06-19 by hedley]


1.1b3 - 2009-03-23
------------------

- Fix git based release problem, now using setuptools-git (hannosch)

1.1b2 - 2009-03-20
------------------

- Tested with Plone 3.0-3.2 [rossp]

- Factor Products/remember/examples/sampleremember to a separate
  Products.sampleremember [rossp]

- Added some CSS classes [hpeteragitator]

- Fix some i18n [khink]

1.1b1 - 2008-08-20
------------------

- Initial release
