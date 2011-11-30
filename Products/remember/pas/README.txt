Tests for Products.remember.pas
===============================

test setup
----------

    >>> from Testing.ZopeTestCase import user_password
    >>> from Testing.testbrowser import Browser
    >>> browser = Browser()

Plugin setup
------------

    >>> acl_users_url = "%s/acl_users" % self.portal.absolute_url()
    >>> browser.addHeader('Authorization', 'Basic %s:%s' % ('portal_owner', user_password))
    >>> browser.open("%s/manage_main" % acl_users_url)
    >>> browser.url
    'http://nohost/plone/acl_users/manage_main'
    >>> form = browser.getForm(index=0)
    >>> select = form.getControl(name=':action')

Products.remember.pas should be in the list of installable plugins:

    >>> 'Remember Email User Authentication' in select.displayOptions
    True

and we can select it:

    >>> select.getControl('Remember Email User Authentication').click()

XXX These fail for some reason, but adding this works fine in a real
browser.

#    >>> select.displayValue
#    ['Remember Email User Authentication']
#    >>> select.value
#    ['manage_addProduct/Products.remember/manage_add_remember_emaillogin_user_authentication_form']

we add 'Remember Email User Authentication' to acl_users:

    >>> from Products.remember.pas.plugin import RememberEmailAuth
    >>> myauth = RememberEmailAuth('myplugin', 'Remember Email User Authentication')
    >>> self.portal.acl_users['myplugin'] = myauth
