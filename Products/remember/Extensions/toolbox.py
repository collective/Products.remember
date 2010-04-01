from App.class_init import InitializeClass

from Products.CMFCore.utils import getToolByName

from Products.remember.utils import getAdderUtility

DEFAULT_WORKFLOW = 'member_auto_workflow'
DEFAULT_CATALOGS = ['portal_catalog', 'membrane_tool']


class SetupMember:

    """
    utility class for configuring members

    call methods separately or in one fell swoop


    0. Setup a member type:

        SetupMember(member_type='Freemason', workflow='Initiation')()


    0. reconfigure a member type:

        reMason = SetupMember(member_type='FreeMason')
        reMason.setWorkflow('Long Initiation')


    0. setup a member, but don't register as the portal default

        SetupMember(member_type='MyMember',
                    is_default=False,
                    register=False).finish()

    """

    def __init__(self, context, member_type, **kw):
        """ context is normally a portal object """
        self.type = member_type
        self.workflow = DEFAULT_WORKFLOW
        self.catalogs = DEFAULT_CATALOGS
        self.is_default = True
        self.register = True
        self.context = context
        if kw:
            self.set(**kw)

    def set(self, **kw):
        [setattr(self, key, val) for key, val in kw.items()]

    def finish(self):
        self.setCatalogs()
        self.setupPortalFactoryProps()
        self.setWorkflow()
        if self.is_default:
            adder = getAdderUtility(self.context)
            adder.default_member_type = self.type

        return "set %s: workflow->%s, catalogs->%s" % (
            self.type, self.workflow, self.catalogs)

    def __call__(self, **kw):
        """ set all, do all """
        if kw:
            self.set(**kw)

        return self.finish()

    def setWorkflow(self, workflow=None):
        if workflow:
            self.workflow = workflow

        wf_tool = getToolByName(self.context, 'portal_workflow')
        wf_tool.setChainForPortalTypes((self.type,), self.workflow)
        wf_tool.updateRoleMappings()

    def setCatalogs(self, catalogs=None):
        if catalogs:
            self.catalogs = catalogs

        at = getToolByName(self.context, 'archetype_tool')
        at.setCatalogsByType(self.type, self.catalogs)

    def setupPortalFactoryProps(self):
        ftool = getToolByName(self.context, 'portal_factory')
        ftypes = ftool.getFactoryTypes()
        if self.type not in ftypes:
            ftypes = ftypes.keys()
            ftypes.append(self.type)
            ftool.manage_setPortalFactoryTypes(listOfTypeIds=ftypes)

InitializeClass(SetupMember)
