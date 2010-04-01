from Products.CMFCore.utils import getToolByName
from Products.remember.utils import log_exc
from Products.remember.utils import trusted


def addWorkflowScripts(wf):
    addProd = wf.scripts.manage_addProduct['ExternalMethod']
    addExternalMethod = addProd.manage_addExternalMethod
    if not 'register' in wf.scripts.objectIds():
        addExternalMethod('register', 'Register a Member',
                          'remember.workflow', 'register')
    if not 'disable' in wf.scripts.objectIds():
        addExternalMethod('disable', 'Disable a Member',
                          'remember.workflow', 'disable')
    if not 'enable' in wf.scripts.objectIds():
        addExternalMethod('enable', 'Enable a Member',
                          'remember.workflow', 'enable')


# Execute the 'trigger' transition -- this should trigger
# any automatic transitions for which the guard conditions
# are satisfied.
def triggerAutomaticTransitions(ob):
    wf_tool = getToolByName(ob, 'portal_workflow')

    # Plone 3 introduces auth problems around creation of private
    # members, wrap action info retrieval with 'trustedness'
    @trusted
    def get_action_ids():
        return [action.get('id', None) for action
                in wf_tool.listActionInfos(object=ob)]
    action_ids = get_action_ids()
    if 'trigger' in action_ids:
        wf_tool.doActionFor(ob, 'trigger')


# set old_state
def disable(self, state_change):
    obj = state_change.object
    try:
        workflow_tool = getToolByName(obj, 'portal_workflow')
        obj.old_state = workflow_tool.getInfoFor(obj, 'review_state', '')
    except:
         # write tracebacks because otherwise workflow will swallow exceptions
        log_exc()
        raise


# Delete old_state
def enable(self, state_change):
    obj = state_change.object
    try:
        if hasattr(obj, 'old_state'):
            delattr(obj, 'old_state')
    except:
        # write tracebacks because otherwise workflow will swallow exceptions
        log_exc()
        raise


# send email with password to  user if necessary
def register(self, state_change):
    obj = state_change.object
    return obj.register()
