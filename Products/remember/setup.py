from setuptools import setup, find_packages
import distext

classifiers = [
    "Programming Language :: Python",
    "Development Status :: 3 - Alpha",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    #{ProductClassifier, text, insertBefore}#,
    ]
setup(
    name             = 'remember',
    author           = 'Rob Miller',
    maintainer       = 'Rob Miller',
    maintainer_email = 'robm@openplans.org',
    url              = "",
    license          = "#{ProductLicense, text, replace}#",
    version          = '0.1',
    platforms        = ["Python >= 2.4", "Zope >= 2.8", "Plone >= 2.1"],
    description      = """A membrane-based Plone member implementation.""",
    classifiers      = classifiers,
    packages         = ['.'] + find_packages(),
    entry_points = {
      'zope2.initialize':
      ['initialize=remember:initialize']
      },

    package_data = {
        'remember':
        ['*', 'conf/*', 'content/*', 'distext/*', 'docs/*', 'Extensions/*', 'skins/*', 'tests/*', 'tools/*']
        },

    zip_safe = False,
    cmdclass = distext.extensions(),
    )
