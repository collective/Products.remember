
QUICK INSTALL

1. Setup requirements for remember and membrane
    e.g. latest Five @ http://codespeak.net/z3/five/release/Five-1.4.2.tgz
2. Add remember and membrane products to your zope Products folder
3. Add sampleremember

QUICK STEPS TO MAKING YOUR OWN PRODUCT BASED ON sampleremember

1. Search and replace all "sampleremember" to "name-of-your-product" (CASE is important)
2. Search and replace all "SampleRemember" to "NameOfYourProduct" (CASE is important)
3. Rename files that are named sampleremember or SampleRemember [list which ones]

MORE INFO:

See "docs/tutorial" for Tutorial documentation.  THIS TUTORIAL IS A BIT DATED and may not include
	all the steps needed.  The 'sampleremember' code is the most up-to-date.

See "examples/sampleremember" for the sample remember product. 

See "examples/sampleremember/TODO.txt" for suggested list of items that need work.

HISTORIC

3/9/07 Tutorial originally created by:

   Andrew Burkhalter <andrewb@onenw.org>
   Brian Gershon <briang@ragingweb.com>


HISTORIC ISSUE (only relates to code based on SampleRemember version 1.0)

a. If you based your code on an earlier version of SampleRemember (v 1.0) you may
  have an incorrectly registered GenericSetup "Import Step" that is stuck
  in your site, which might be preventing other GenericSetup profiles from running.
  
  I posted a How-To on plone.org called "GenericSetup: Uninstalling Import Steps" (which
  also details doing this manually in Clouseau), but if you're anxious:

  NOTE: The bad step may be called "remember-useraddr" or "sampleremember-defaultmember"
        or it may be called "YourProductNameHere-default".
        
        The correct one is "remember-useradder", so don't delete that one.
  
  Instructions for removing this step are to create an External Method
  that calls the following code:  
  
  from Products.GenericSetup import profile_registry, EXTENSION
  from Products.CMFPlone.interfaces import IPloneSiteRoot
  from Products.CMFCore.utils import getToolByName
  
  setup = getToolByName(self, 'portal_setup')
  
  setup.setImportContext('profile-myproduct:default')
  
  ir = setup.getImportStepRegistry()
  #print ir.listSteps()  # for debugging and seeing what steps are available
  
  # delete the offending step
  try:
      del ir._registered['myproduct-badstep']
  except KeyError:
      pass
  # commit the changes to the zodb
  import transaction
  txn = transaction.get()
  txn.commit()
