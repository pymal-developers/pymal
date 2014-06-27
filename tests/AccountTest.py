import unittest

from pymal import Account
from pymal.account_objects import AccountMangas
from pymal.account_objects import AccountAnimes

from tests.constants_for_testing import ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD


class InitTestCase(unittest.TestCase):

    def test_init_not_auth(self):
        account = Account.Account(ACCOUNT_TEST_USERNAME)
        self.assertFalse(account.is_auth)
        Account.Account._unregiter(account)

    def test_account_init_auth(self):
        account = Account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        self.assertTrue(account.is_auth)
        Account.Account._unregiter(account)

    def test_init_auth_bad_password(self):
        account = Account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD * 2)
        self.assertFalse(account.is_auth)
        Account.Account._unregiter(account)

    def test_init_later_auth(self):
        account = Account.Account(ACCOUNT_TEST_USERNAME)
        self.assertFalse(account.is_auth)

        account.change_password(ACCOUNT_TEST_PASSWORD)
        self.assertTrue(account.is_auth)
        Account.Account._unregiter(account)

    def test_init_later_auth_bad_password(self):
        account = Account.Account(ACCOUNT_TEST_USERNAME)
        self.assertFalse(account.is_auth)

        self.assertFalse(account.change_password(ACCOUNT_TEST_PASSWORD * 2))
        self.assertFalse(account.is_auth)
        Account.Account._unregiter(account)

    def test_str_no_password(self):
        account = Account.Account(ACCOUNT_TEST_USERNAME)
        self.assertEqual(str(account), "<Account username: pymal-developr>")
        Account.Account._unregiter(account)

    def test_str_with_password(self):
        account = Account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        self.assertEqual(str(account), "<Account username: pymal-developr>")
        Account.Account._unregiter(account)

    def test_user_id(self):
        account = Account.Account(ACCOUNT_TEST_USERNAME)
        self.assertEqual(account.user_id, 3854655)
        Account.Account._unregiter(account)


class FunctionsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.account = Account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)

    @classmethod
    def tearDownClass(cls):
        Account.Account._unregiter(cls.account)

    def test_reload(self):
        self.assertIsInstance(self.account.animes, AccountAnimes.AccountAnimes)
        self.assertIsInstance(self.account.mangas, AccountMangas.AccountMangas)

    def test_username(self):
        self.assertEqual(self.account.username, ACCOUNT_TEST_USERNAME)

    def test_friends(self):
        self.assertIsInstance(self.account.friends, set)
        for friend in self.account.friends:
            self.assertIsInstance(friend, Account.Account)
            self.assertIn(self.account, friend.friends)


def main():
    unittest.main()


if '__main__' == __name__:
    main()