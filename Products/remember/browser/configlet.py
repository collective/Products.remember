from zope.interface import Interface
from zope import schema
from zope.formlib import form
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('remember')

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
try:
    from Products.Five.formlib.formbase import PageForm
    PageForm  # pyflakes
except ImportError:
    from zope.formlib.form import PageForm

from Products.remember.utils import getAdderUtility


class IRememberConfiglet(Interface):
    default_mem_type = schema.Choice(
        title=_(u'Default Member Type'),

        description=_(u'This specifies the default member type for remember.'),
        required=True,
        vocabulary='RememberTypes',
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

    def getDefaultMemType(self):
        adder = getAdderUtility(self.context)
        return adder.default_member_type

    form_fields['default_mem_type'].get_rendered = getDefaultMemType
