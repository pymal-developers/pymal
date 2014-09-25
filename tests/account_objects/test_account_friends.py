import unittest

from pymal import account

from tests.constants_for_testing import ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD


class InitTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.account = account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)

    @classmethod
    def tearDownClass(cls):
        account.Account._unregiter(cls.account)

    def test_friends(self):
        for friend in self.account.friends:
            self.assertIsInstance(friend, account.Account)
            self.assertIn(self.account, friend.friends)


def main():
    unittest.main()


if '__main__' == __name__:
    main()