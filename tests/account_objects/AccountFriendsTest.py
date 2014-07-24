import unittest

from pymal import Account

from tests.constants_for_testing import ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD


class InitTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.account = Account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)

    @classmethod
    def tearDownClass(cls):
        Account.Account._unregiter(cls.account)

    def test_friends(self):
        for friend in self.account.friends:
            self.assertIsInstance(friend, Account.Account)
            self.assertIn(self.account, friend.friends)


def main():
    unittest.main()


if '__main__' == __name__:
    main()