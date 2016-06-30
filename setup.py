from setuptools import setup, find_packages

version = '1.9.4'
tests_require = [
    'collective.testcaselayer',
    'plone.browserlayer',
    'Products.PloneTestCase',
    'zope.testbrowser>3.3',
]

setup(
    name='Products.remember',
    version=version,
    description="""\
A content-based implementation of Plone's default member infrastructure""",
    long_description=(
        open("README.rst").read() + "\n" +
        open("CHANGES.rst").read()
    ),
    # Get more strings from
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 6 - Mature",
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
        'Products.membrane>=2.0',
    ],
    tests_require=tests_require,
    extras_require={'test': tests_require},
    )
