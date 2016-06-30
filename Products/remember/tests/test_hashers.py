import unittest

from zope.annotation.interfaces import IAnnotations
from zope.component import getAdapter

from Products.CMFCore.utils import getToolByName
from Products.remember.interfaces import IHashPW
from Products.remember.config import HASHERS
from Products.remember.config import ANNOT_KEY

from base import RememberTestBase
from base import def_mem_data
from base import mem_data

MEM_DATA = def_mem_data.copy()
MEM_DATA.update(mem_data['portal_member'])


class TestHasher(RememberTestBase):
    """
    test the different hashing methods available
    """

    def test_hashers(self):
        for htype in HASHERS:
            login_id = 'hashtest_%s' % htype
            member = self.portal_member
            if not getAdapter(member, IHashPW, htype).isAvailable():
                continue

            mbtool = getToolByName(member, 'membrane_tool')
            annot = IAnnotations(mbtool)
            annot.setdefault(ANNOT_KEY, {})['hash_type'] = htype
            member.setRoles('Member')
            member.processForm(values=MEM_DATA)

            password = member.getPassword()
            hash_type, hashed = password.split(':', 1)

            self.assertEqual(htype, hash_type)
            self.failUnless(member.verifyCredentials(
                dict(login='portal_member', **MEM_DATA)))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestHasher))
    return suite
