from zope.schema.vocabulary import SimpleVocabulary

from Products.remember.utils import getRememberTypes


def rememberTypes(context):
    """
    Returns a vocabulary of the remember member types.
    """
    remtypes = getRememberTypes(context)
    remtypes.sort()
    remtypes = [(i, i) for i in remtypes]
    return SimpleVocabulary.fromItems(remtypes)
