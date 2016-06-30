from Products.remember.config import PROJECT_NAME

REPLACE_CMFMEMBER_WORKFLOWS = True

"""
The following data structure contains the info needed for migrations
from CMFMember-based member objects to those that are remember-based.
The keys of the dictionary should be the dotted names of the classes
of the new member types.  Each value of the dictionary should be
another dictionary, with the following key/value pairs:

atct_newTypeFor: This will be dynamically added (i.e. 'monkeypatched')
                 as an _atct_newTypeFor attribute on the new class,
                 used by the ATCT and contentmigration infrastructure
                 that we use.  The value should be a dictionary
                 containing the portal_type and meta_type of the OLD
                 member type (i.e. the one you are migrating FROM).

project_name: This should contain the name of the Zope product with
              which the new member type will be associated.

profile: This should contain the name of the GenericSetup profile that
         must be imported to install the new member types and any
         associated workflows, site customizations, etc.  You should
         either add an entry for 'profile' or 'product', but not both.
         (It both are defined, 'profile' will be used and 'product'
         will be ignored.)

product: This should contain the name of the CMFQuickInstaller product
         that should be installed in order to install the new member
         types and any associated workflows, site customizations, etc.
         You should either add an entry for 'profile' or 'product',
         but not both.  (It both are defined, 'profile' will be used
         and 'product' will be ignored.)

replace_workflows: This should be a boolean value.  If True, then the
                   workflows specified in the 'workflow_ids' value
                   will be deleted prior to importing the new profile
                   (or installing the new product).  The assumption is
                   that the new profile or product will replace the
                   workflows with newer implementations.

workflow_ids: This should be an iterator containing the ids of the
              workflows to be deleted before the new profile/product
              is imported/installed.  If 'replace_workflows' is set
              to False, this value will be ignored.
"""

MIGRATION_MAP = {
    'Products.remember.content.Member':
    {'atct_newTypeFor': {'portal_type': 'Member',
                         'meta_type': 'Member'},
     'project_name': PROJECT_NAME,
     'profile': 'profile-remember:default',
     'replace_workflows': REPLACE_CMFMEMBER_WORKFLOWS,
     'workflow_ids': ('member_auto_workflow',
                      'member_approval_workflow'),
     },
}
