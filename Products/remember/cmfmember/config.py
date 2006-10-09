from Products.remember.content import Member
from Products.remember.config import PROJECT_NAME

REPLACE_CMFMEMBER_WORKFLOWS = True

MIGRATION_MAP = {
    Member: {'atct_newTypeFor': {'portal_type': 'Member',
                                 'meta_type': 'Member'},
             'project_name': PROJECT_NAME,
             'profile': 'profile-remember:default',
             'replace_workflows': REPLACE_CMFMEMBER_WORKFLOWS,
             'workflow_ids': ('member_auto_workflow',
                              'member_approval_workflow'),
             }
    }
