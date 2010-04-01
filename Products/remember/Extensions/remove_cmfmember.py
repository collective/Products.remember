from Products.CMFCore.utils import getToolByName

keep_types = ('MemberDataContainer', 'Member')


def remove_cmfmember(self):
    qi = getToolByName(self, 'portal_quickinstaller')

    if qi.isProductInstalled('CMFMember'):
        # don't let CMFMember remove stuff we want to keep
        cmfm_prod = qi.CMFMember
        for ktype in keep_types:
            if ktype in cmfm_prod.types:
                cmfm_prod.types.remove(ktype)
        cmfm_prod.workflows = []  # triggers persistence

        # uninstall the product
        qi.uninstallProducts(products=['CMFMember'])

    # clean up the portlets in portal_memberdata
    mdtool = getToolByName(self, 'portal_memberdata')
    oldslots = mdtool.getProperty('left_slots')
    newslots = []
    for slot in oldslots:
        if not slot.startswith('here/portlet_cmfmember'):
            newslots.append(slot)
        elif slot == 'here/portlet_cmfmember/macros/portlet_prefs_wrapper':
            newslots.append('here/portlet_prefs/macros/portlet')
    mdtool.manage_changeProperties(left_slots=newslots)

    # remove spurious "copy_of_Member" type
    ttool = getToolByName(self, 'portal_types')
    if ttool.hasObject('copy_of_Member'):
        ttool.manage_delObjects(['copy_of_Member'])

    return "CMFMember removed"
