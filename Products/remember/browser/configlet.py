from zope.interface import Interface
from zope import schema
from zope.formlib import form
from zope.schema.vocabulary import SimpleVocabulary
from zope.i18nmessageid import MessageFactory
_  = MessageFactory('remember')

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
try: from Products.Five.formlib.formbase import PageForm
except ImportError: from zope.formlib.form import PageForm

from Products.remember.utils import getAdderUtility
from Products.remember.config import DEFAULT_MEMBER_TYPE


class IRememberConfiglet(Interface):
    default_mem_type = schema.Choice(
        title=_(u'Default Member Type'),
        
        description=_(u'This specifies the default member type for remember.'),
        required=True,
        vocabulary='RememberTypes',
        )

    email_login = schema.Bool(
        title=_(u'Members log in with their email addresses'),
        description=_(u'Check this box if you want users to be able to login \
                with their email addresses. If you change this value but \
                already have members in your site then you must update the \
                membrane_tool catalog.'),
        )

class RememberConfiglet(PageForm):
    """
    The formlib class for the remember config page.
    """
    template = ViewPageTemplateFile('configletform.pt')

    form_fields = form.FormFields(IRememberConfiglet)

    @form.action("submit")
    def action_submit(self, action, data):
        adder = getAdderUtility(self.context)
        adder.default_member_type = data['default_mem_type']
        adder.email_login = data['email_login']

    def getDefaultMemType(self):
        adder = getAdderUtility(self.context)
        return adder.default_member_type

    def getEmailLogin(self):
        adder = getAdderUtility(self.context)
        return adder.email_login

    form_fields['default_mem_type'].get_rendered = getDefaultMemType
    form_fields['email_login'].get_rendered = getEmailLogin
