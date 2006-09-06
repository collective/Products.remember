"""Membership tool properties setup handlers.

$Id:$
"""

from zope.app import zapi
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.interfaces import IBody

_FILENAME = 'membership_properties.xml'

def importMembershipProperties(context):
    """ Import Membership tool properties.
    """
    site = context.getSite()
    logger = context.getLogger('membership properties')
    ptool = getToolByName(site, 'portal_membership')

    body = context.readDataFile(_FILENAME)
    if body is None:
        logger.info('Membership tool: Nothing to import.')
        return

    importer = zapi.queryMultiAdapter((ptool, context), IBody)
    if importer is None:
        logger.warning('Membership tool: Import adapter misssing.')
        return

    importer.body = body
    logger.info('Membership tool imported.')

def exportMembershipProperties(context):
    """ Export Membership tool properties .
    """
    site = context.getSite()
    logger = context.getLogger('membership properties')
    ptool = getToolByName(site, 'portal_membership', None)
    if ptool is None:
        logger.info('Membership tool: Nothing to export.')
        return

    exporter = zapi.queryMultiAdapter((ptool, context), IBody)
    if exporter is None:
        logger.warning('Membership tool: Export adapter misssing.')
        return

    context.writeDataFile(_FILENAME, exporter.body, exporter.mime_type)
    logger.info('Membership tool exported.')

