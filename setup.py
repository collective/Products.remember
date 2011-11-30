from setuptools import setup, find_packages
import os

version = open(os.path.join('Products', 'remember', 'version.txt')).read()

setup(name='Products.remember',
      version=version,
      description="A content-based implementation of Plone's default member infrastructure",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 3.2",
        "Framework :: Plone :: 3.3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Rob Miller',
      author_email='robm@openplans.org',
      url='http://plone.org/products/remember',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.membrane>=1.1dev,<2.0dev',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
