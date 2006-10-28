===========================================
remember
===========================================

:author: Rob Miller
:date: 03/27/2006
:version: Version 0.1



Introduction
~~~~~~~~~~~~

The big picture: What does this product do?  What problem(s) does it solve?
Who is it intended for?

Using remember
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

How does one use this used?

Code overview
~~~~~~~~~~~~~

A high level sketch of the main code components and how they interact.

Code details
~~~~~~~~~~~~

Any details of the code's operation that are particularly useful 

Are there any settings that need configuring on installation?

Code Layout
~~~~~~~~~~~

::

 /Project/
        /content
        /docs
        /Extensions
        /lib
        /skins/
                /projectskin
        /tests/
        /tools

        README.txt
        __init__.py
        config.py
        permissions.py
        version.txt



Descriptions of each project element follow:

content/
        Projects that introduce content types should place each
        content types implementation in a file in this directory.

distext/
        Infrastructure used in package management.

doc/
        Information about installing and using your product go here

Extensions/
        The installer for your product goes here and will be used by
        the QuickInstaller product to easily add/remove your product from a
        site.

lib/
        Library level code for this project. Many projects only
        introduce skins and content types and will not need to include a lib
        directory.

skins/
        PageTemplates, Python scripts and static content (typically
        images) related to your project go into subdirectories here with names
        that make sense to you.

tests/
        Every project should include tests of new features and code
        that it introduces. Plone and Archetypes leverage powerful testing
        frameworks that make this simple to do. It speeds development and
        saves debugging time.

tools/
        If your project provides additional tools you might include
        those here.


README.txt
        Your projects letter of introduction.

__init__.py
        Includes boilerplate code that will register the project
        elements with Zope and Archetypes as needed.


config.py
        Typically I use config.py to include static definitions and
        variables that are the product of import time decisions. config.py
        should contain only immutable variables as a matter of convention.

permissions.py
        If you require additional security permissions for your new
        content or tools it is suggested you place them here

version.txt
        A simple text file containing a version string used when
        talking about the product.

Workflows
~~~~~~~~~

When creating a new workflow the "Copy or Move" must be restricted to Manager for each state of the workflow.  If this is not done then the user will see "Copy" in object actions dropdown when looking at a member object.


