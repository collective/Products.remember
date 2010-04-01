def NoneFileSystemExporter(context):
    """
    Adapter to make portal_setup/manage_createSnapshot work with remember

    Question:

    remember seems to break portal_setup/manage_createSnapshot. Before
    installing remember it works fine, after I get a "BadRequest: The id
    "portal_memberdata" is reserved. " Any ideas?

    Answer:

    the problem is that remember replaces the default portal_memberdata w/ one
    that subclasses ATBTreeFolder
    the key is on line 114 of the Products.CMFCore.exportimport.content module
    adapter = IFilesystemExporter(object, None)    <---- this adaptation needs
    to return None, but it's not doing so b/c there IS an adapter registered
    for contentish BTree folders
    so a workaround would be to register a more specific adapter, with
    a factory method that simply returns "None"
    something that adapts from IMemberDataTool -> IFilesystemExporter
    so you register the adapter, and instead of using a class as the factory,
    you use a function that just returns None
    i think that solution is fine... if you get it to work, it can go directly
    into remember
    i'd put it in the Products.remember.exportimport package
    """

    return None
