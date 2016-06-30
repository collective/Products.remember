"""Provides migrators that can be used by products that define custom
contentish members to migrate from CMFMember to remember."""
import logging

from Acquisition import aq_base
from AccessControl.AuthEncoding import is_encrypted

from Products.CMFCore.utils import getToolByName

from Products.Archetypes.ArchetypeTool import getType
from Products.Archetypes.utils import shasattr
from Products.Archetypes.Extensions.utils import filterTypes
from Products.Archetypes.Extensions.utils import install_types

from Products.ATContentTypes.migration.common import registerATCTMigrator
from Products.ATContentTypes.migration.walker import CatalogWalker
from Products.ATContentTypes.migration.common import migratePortalType

from Products.contentmigration.archetypes import InplaceATItemMigrator
from Products.contentmigration.translocate import TranslocatingInplaceMigrator

from config import MIGRATION_MAP

migrators = []


def getClassFromClassPath(classpath):
    module_name = '.'.join(classpath.split('.')[:-1])
    classname = classpath.split('.')[-1]
    klass = getattr(__import__(module_name, globals(),
                               locals(), classname),
                    classname)
    return klass


class CMFMemberMigrator(TranslocatingInplaceMigrator,
                        InplaceATItemMigrator):
    walkerClass = CatalogWalker

    def log(self, level, msg, *args, **kwargs):
        """Write to event log."""
        logger = logging.getLogger('remember.cmfmember')
        logger.log(level, msg, *args, **kwargs)

    def getDestinationParent(self):
        """Return the container into which the destination will be
        added."""
        purl = getToolByName(self.parent, 'portal_url')
        portal = purl.getPortalObject()
        tmp_pmd = portal.cmfmember_tmp.portal_memberdata
        if aq_base(self.parent) is aq_base(tmp_pmd):
            return getToolByName(portal, 'portal_memberdata')
        else:
            return self.parent

    def patchUserInfo(self):
        """Update the member._userInfo attribute to reflect the moving
        of portal.acl_users into the temporary folder."""
        if self.old._userInfo is None:
            msg = "Can't patch %s _userInfo" % self.old.getId()
            self.log(logging.WARNING, msg)
            return
        path, id = self.old._userInfo
        purl = getToolByName(self.parent, 'portal_url')
        portal = purl.getPortalObject()

        # if the acl_users we get from the userInfo path is the same
        # one as we get from getToolByName for the portal then we
        # patch the path
        portal_acl_users = getToolByName(portal, 'acl_users')
        acl_users = portal.unrestrictedTraverse(path)
        if aq_base(portal_acl_users) is aq_base(acl_users):
            path = 'cmfmember_tmp/' + path
        self.old._userInfo = (path, id)

        # If getUser has already been called then the result of
        # previous calls is cached in _v_user so we remove it
        if shasattr(self.old, '_v_user'):
            del self.old._v_user

    def migrate(self, *args, **kw):
        """We need to correct the self._userInfo attribute since we've
        moved the GRUF acl_users."""
        msg = 'Migrating: %s' % self.old.getId()
        self.log(logging.INFO, msg)
        self.patchUserInfo()
        return InplaceATItemMigrator.migrate(self, *args, **kw)

    def beforeChange_password(self):
        """The CMFMember password field has mode 'w' so we need to put
        it in the schema kwargs here."""
        kwargs = getattr(self, 'schema', {})
        kwargs['password'] = self.old.getPassword()
        self.schema = kwargs

    def migrate_password(self):
        """If the original password was encrypted, we don't want to
        re-encrypt during the migration."""
        # migration will have already happened correctly if the
        # password wasn't encrypted
        old_pw = self.old.getPassword()
        if is_encrypted(old_pw):
            field = self.new.getField('password')
            new_pw = "zauth:%s" % old_pw
            field.set(self.new, new_pw)  # don't use mutator!


def registerCMFMemberMigrator(migrator, klass, project_name):
    """Register a migrator for migrating CMFMember based content to
    remember based content.  Migrators registered here will be run on
    Plone 2.5 migration if enabled."""

    registerATCTMigrator(migrator, klass)

    def migrateCMFMemberType(portal, out):
        """Run the actual migration."""

        src_portal_type = klass._atct_newTypeFor['portal_type']
        dst_portal_type = klass.portal_type

        # store the workflow(s) associated w/ the old type so we can
        # associate the new one when we're done
        wftool = getToolByName(portal, 'portal_workflow')
        chain = wftool.getChainForPortalType(src_portal_type)

        # portal_quickinstaller won't work before the membrane_tool is
        # in place because some remember fields are indexed in the
        # membrane_tool but it isn't installed before migration.  So
        # we use Archetypes to install the type here.
        ttool = getToolByName(portal, 'portal_types')
        dst = ttool.getTypeInfo(dst_portal_type)
        if dst is None:
            print >> out, ("...installing %s type"
                           % dst_portal_type)
            at_type = getType(klass.meta_type, project_name)
            types = filterTypes(portal, out, [at_type], project_name)
            install_types(portal, out, types, project_name)

        mt = getToolByName(portal, 'membrane_tool')
        if dst_portal_type not in mt.listMembraneTypes():
            print >> out, ("...registering %s with membrane_tool"
                           % dst_portal_type)
            mt.registerMembraneType(dst_portal_type)

        print >> out, "...migrating %s to %s" % (src_portal_type,
                                                 dst_portal_type)
        migratePortalType(portal,
                          src_portal_type=src_portal_type,
                          dst_portal_type=dst_portal_type,
                          migrator=migrator,
                          use_catalog_patch=False)

        # associate the appropriate workflow
        wftool.setChainForPortalTypes((dst_portal_type,),
                                      chain)

    migrators.append(migrateCMFMemberType)


def migrateCMFMembers(portal, out):
    """Run all the registered CMFMember migrators."""
    print >> out, "...running all CMFMember migrators"
    for migrator in migrators:
        migrator(portal, out)


def registerMigrators():
    for classpath, info in MIGRATION_MAP.items():
        klass = getClassFromClassPath(classpath)
        klass._atct_newTypeFor = info['atct_newTypeFor']
        registerCMFMemberMigrator(CMFMemberMigrator,
                                  klass, info['project_name'])
