from Products.CMFCore.utils import getToolByName
from Products.remember.utils import log_exc

# Execute the 'trigger' transition -- this should trigger
# any automatic transitions for which the guard conditions
# are satisfied.
def triggerAutomaticTransitions(ob):
    wf_tool=getToolByName(ob, 'portal_workflow')
    if 'trigger' in [action.get('id',None) for action in wf_tool.getActionsFor(ob)]:
        wf_tool.doActionFor(ob, 'trigger')

# set old_state
def disable(self, state_change):
    obj=state_change.object
    try:
        workflow_tool = getToolByName(obj, 'portal_workflow')
        obj.old_state = workflow_tool.getInfoFor(obj, 'review_state', '')
    except:
         # write tracebacks because otherwise workflow will swallow exceptions
        log_exc()
        raise

# Delete old_state
def enable(self, state_change):
    obj=state_change.object
    try:
        if hasattr(obj, 'old_state'):
            delattr(obj, 'old_state')
    except:
        # write tracebacks because otherwise workflow will swallow exceptions
        log_exc()
        raise
