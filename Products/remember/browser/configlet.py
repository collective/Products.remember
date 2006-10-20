from zope.interface import Interface
from zope import schema
from zope.formlib import form
from zope.schema.vocabulary import SimpleVocabulary
from zope.i18nmessageid import MessageFactory
_  = MessageFactory('remember')

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
try: from Products.Five.formlib.formbase import PageForm
except ImportError: from zope.formlib.form import PageForm

from Products.membrane.interfaces import IUserAdder
from Products.remember.config import DEFAULT_MEMBER_TYPE
from Products.remember.config import ADDUSER_UTILITY_NAME

class IRememberConfiglet(Interface):
    default_mem_type = schema.Choice(title=_(u'Default Member Type'),
                                     description=_(u'Default Member Type'),
                                     required=True,
                                     vocabulary='RememberTypes',
                                     default=_(unicode(DEFAULT_MEMBER_TYPE)),
                                     )


class RememberConfiglet(PageForm):
    """
    The formlib class for the remember config page.
    """
    template = ZopeTwoPageTemplateFile('configletform.pt')

    form_fields = form.FormFields(IRememberConfiglet)

    @form.action("submit")
    def action_submit(self, action, data):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        sm = portal.getSiteManager()
        adder = sm.queryUtility(IUserAdder, ADDUSER_UTILITY_NAME)
        if adder is None:
            raise(RuntimeError, "Unable to retrieve IUserAdder utility")

        adder.default_member_type = data['default_mem_type']
