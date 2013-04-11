import unittest

from DateTime.DateTime import DateTime

from base import our_num_remem_mems
from base import all_mems
from base import RememberTestBase


class TestRememberSearching(RememberTestBase):
    """
    verify searching for members
    """

    def testSearchAll(self):
        """
        verify that searching without any constraints returns all
        members
        """
        results = self.mtool.searchForMembers()
        self.assertEqual(len(results), all_mems)

    def testSearchByName(self):
        """
        check searching for members for different queries
        """
        results = self.mtool.searchForMembers(login='portal_member')
        self.assertEqual(len(results), 1)
        self.assertEqual('portal_member', results[0].getId())

    def testSearchByNameWithLoginTime(self):
        """
        search for the last login time, similar to how the search page
        does it on the form
        """
        self.mtool.setLoginTimes()
        dt = DateTime('2/1/2000')
        results = self.mtool.searchForMembers(
            login='portal_member',
            getLast_login_time=dt,
            getLast_login_time_usage='range:min')
        self.assertEqual(len(results), 1)
        self.assertEqual('portal_member', results[0].getId())

    def testSearchLoginTime(self):
        """
        search for the last login time for members that haven't logged
        in yet this simulates the 'not logged in since specified'
        checkbox on the search form
        """
        self.mtool.setLoginTimes()
        results = self.mtool.searchForMembers(
            last_login_time=DateTime('2/1/2000'),
            before_specified_time=True)
        # portal member is not in all list because is logged in
        self.assertEqual(len(results), all_mems - 1)

    def testSearchForFailingLogin(self):
        """
        search for a login that is illegitimate.
        no members should be found
        """
        results = self.mtool.searchForMembers(
            login='halstingdingdingworth')  # this guy shouldn't exist
        self.failIf(len(results))

    def testSearchByEmail(self):
        """
        validate searching by email
        """
        results = self.mtool.searchForMembers(
            email='noreply@xxxxxxxxyyyyyy.com')
        self.assertEqual(len(results), our_num_remem_mems)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRememberSearching))
    return suite
