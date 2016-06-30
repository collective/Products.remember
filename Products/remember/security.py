from Products.CMFCore.utils import getToolByName

from plone.app.controlpanel import security


class SecurityControlPanelAdapter(
        security.SecurityControlPanelAdapter):

    def set_enable_self_reg(self, value):
        super(SecurityControlPanelAdapter, self
              ).set_enable_self_reg(value)

        md = getToolByName(self.portal, 'portal_memberdata')

        reg_roles = []
        if value == True and 'Anonymous' not in reg_roles:
            reg_roles.append('Anonymous')
        if value == False and 'Anonymous' in reg_roles:
            reg_roles.remove('Anonymous')

        try:
            app_perms = md.rolesOfPermission(permission='Add portal content')
        except ValueError:
            # XXX remember probably not quick installed, skip the rest.
            return
        for appperm in app_perms:
            if appperm['selected'] == 'SELECTED':
                reg_roles.append(appperm['name'])
        md.manage_permission('Add portal content', roles=reg_roles, acquire=0)

    enable_self_reg = property(
        security.SecurityControlPanelAdapter.get_enable_self_reg,
        set_enable_self_reg)

    def set_enable_user_pwd_choice(self, value):
        super(SecurityControlPanelAdapter, self
              ).set_enable_user_pwd_choice(value)

        props = getToolByName(self.portal, 'portal_properties')
        if value == True:
            props.site_properties.validate_email = False
        else:
            props.site_properties.validate_email = True

    enable_user_pwd_choice = property(
        security.SecurityControlPanelAdapter.get_enable_user_pwd_choice,
        set_enable_user_pwd_choice)
