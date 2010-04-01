"""Patches to the PlonePAS installer for migrating a CMFMember pre-2.5
Plone site to a remember 2.5 or later Plone site."""

import os

from Acquisition import aq_base

from Products.CMFCore.utils import getToolByName

from Products.CMFPlone.migrations.v2_5.betas import installPortalSetup
from Products.CMFPlone.migrations.v2_5 import alphas
from Products.CMFPlone.migrations.migration_util import (
    installOrReinstallProduct)

from Products.PlonePAS.Extensions import Install as InstallPlonePAS
from Products.PlonePAS.Extensions.Install import addPAS
from Products.PlonePAS.Extensions.Install import updateProp
from Products.PlonePAS.tools.memberdata import MemberDataTool

from Products.contentmigration.utils import unrestricted_move


################################################
# prepare member classes for migration registry
################################################

from config import MIGRATION_MAP
from migrator import migrateCMFMembers


################################################
# from CMFPlone.migrations.v2_5.alphas
################################################
def installPlonePAS(portal, out):
    """We have to install PlonePAS by calling the function directly
    instead of through QuickInstaller because our patches won't take
    if the function is called as an ExternalMethod."""
    NO_PLONEPAS = os.environ.get('SUPPRESS_PLONEPAS_INSTALLATION',
                                 None) == 'YES'
    if NO_PLONEPAS:
        return

    origGrabUserData = InstallPlonePAS.grabUserData
    origReplaceUserFolder = InstallPlonePAS.replaceUserFolder
    origMigrateMemberDataTool = InstallPlonePAS.migrateMemberDataTool
    origRestoreUserData = InstallPlonePAS.restoreUserData

    # we assume the remember migration is desired if CMFMember is
    # installed
    qi = getToolByName(portal, 'portal_quickinstaller')
    HAS_CMFMEMBER = qi.isProductInstalled('CMFMember')
    if HAS_CMFMEMBER:
        InstallPlonePAS.grabUserData = grabUserData
        InstallPlonePAS.replaceUserFolder = replaceUserFolder
        InstallPlonePAS.migrateMemberDataTool = migrateMemberDataTool
        InstallPlonePAS.restoreUserData = restoreUserData

    installOrReinstallProduct(portal, 'PasswordResetTool', out)

    if HAS_CMFMEMBER:
        # run the installer directly and undo the patches
        result = InstallPlonePAS.install(portal)
        out.extend(result.split('\n'))

        InstallPlonePAS.grabUserData = origGrabUserData
        InstallPlonePAS.replaceUserFolder = origReplaceUserFolder
        InstallPlonePAS.migrateMemberDataTool = origMigrateMemberDataTool
        InstallPlonePAS.restoreUserData = origRestoreUserData
    else:
        installOrReinstallProduct(portal, 'PlonePAS', out)


################################################
# From PlonePAS.Extensions.Install
################################################
def grabUserData(portal, out):
    """User data is contained in the contentish members so we don't
    need to grab any user data."""
    print >> out, "\nSkipping Member information extraction..."


def replaceUserFolder(portal, out):
    print >> out, ("\nUser folder replacement from CMFMember to "
                   "remember:")

    print >> out, " - Creating temporary folder"
    portal.invokeFactory('Folder', 'cmfmember_tmp')

    print >> out, (" - Moving existing user folder into temporary "
                   "folder")

    unrestricted_move(portal.cmfmember_tmp, portal.acl_users)
    addPAS(portal, out)

    print >> out, "...replace done"


def migrateMemberDataTool(portal, out):
    print >> out, ("MemberData Tool (portal_memberdata) from "
                   "CMFMember to remember")

    print >> out, " ...move MemberData Tool to temporary folder"
    unrestricted_move(portal.cmfmember_tmp, portal.portal_memberdata)

    ps_out = []
    installPortalSetup(portal, ps_out)
    print >> out, '\n'.join(ps_out)

    # Need CMFMember Member Type Info out of the way for GenericSetup
    # steps
    pt = getToolByName(portal, 'portal_types')
    wft = getToolByName(portal, 'portal_workflow')

    mig_map_values = MIGRATION_MAP.values()

    print >> out, " ...moving old member types and workflows out of the way"
    for info in mig_map_values:
        mem_type = info['atct_newTypeFor']['portal_type']
        chain = wft.getChainForPortalType(mem_type)
        info['chain'] = chain
        unrestricted_move(portal.cmfmember_tmp,
                          getattr(pt, mem_type))
        if info.get('replace_workflows', False):
            wf_ids = info['workflow_ids']
            for wf_id in wf_ids:
                wft._delObject(wf_id)

    ps = getToolByName(portal, 'portal_setup')
    qi = getToolByName(portal, 'portal_quickinstaller')

    # need to instantiate a default MemberDataTool since changes to
    # GenericSetup mean the membrane profile is no longer doing so,
    # but it will fail if there isn't one
    if portal._getOb('portal_memberdata', None) is None:
        mdtool = MemberDataTool()
        portal._setObject('portal_memberdata', mdtool)

    print >> out, " ...applying membrane profile"
    ps.setImportContext('profile-CMFPlone:plone')
    ps.setImportContext('profile-membrane:default')
    ps.runAllImportSteps()

    print >> out, " ...applying new member implementation profiles"
    for info in mig_map_values:
        profile = info.get('profile', None)
        product = info.get('product', None)
        if profile is not None:
            ps.setImportContext(profile)
            ps.runAllImportSteps()
        elif product is not None:
            # use a QI install method instead
            if not qi.isProductInstalled(product):
                qi.installProduct(product)
            else:
                qi.reinstallProducts([product])

    print >> out, " ...restoring old member types"
    # Needed for the actual member migration
    for info in mig_map_values:
        mem_type = info['atct_newTypeFor']['portal_type']
        unrestricted_move(pt, getattr(portal.cmfmember_tmp, mem_type))
        wft.setChainForPortalTypes((mem_type,), info['chain'])

    if hasattr(aq_base(portal.cmfmember_tmp.portal_memberdata),
               '_actions'):
        print >> out, " ...migrating actions"
        actions = portal.cmfmember_tmp.portal_memberdata._actions
        portal.portal_memberdata._actions = actions

    print >> out, " ...migrating data"
    mdtool = portal.cmfmember_tmp.portal_memberdata
    properties = mdtool._properties
    for elt in properties:
        elt['value'] = mdtool.getProperty(elt['id'])
        updateProp(portal.portal_memberdata, elt)

    print >> out, " ...done"


def restoreUserData(portal, out, userdata):
    print >> out, ("\nMigrating CMFMember content to remember "
                   "content...")
    migrateCMFMembers(portal, out)

    print >> out, "...restore done, removing temporary"
    portal.manage_delObjects(['cmfmember_tmp'])

    print >> out, " ...done"

origInstallPlonePAS = alphas.installPlonePAS
alphas.installPlonePAS = installPlonePAS
