from setuptools import setup, find_packages
import os

version = '1.9b2'
tests_require = ['collective.testcaselayer',
                 'plone.browserlayer',
                 'zope.testbrowser>3.3']

setup(name='Products.remember',
      version=version,
      description="""\
A content-based implementation of Plone's default member infrastructure""",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Other Audience",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        ],
      keywords='plone membrane membership content remember',
      author='Rob Miller',
      author_email='robm@openplans.org',
      maintainer='Ken Manheimer',
      maintainer_email='Ken.Manheimer@gmail.com',
      url='http://plone.org/products/remember',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.membrane>=2.0dev',
          # -*- Extra requirements: -*-
      ],
      tests_require=tests_require,
      extras_require={'test': tests_require},
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
