import unittest

from pymal import Account
from pymal import AccountAnimes
from pymal import AccountMangas

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


class FunctionsTestCase(unittest.TestCase):

    def setUp(self):
        self.account = Account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)

    def test_reload(self):
        self.assertIsInstance(self.account.animes, AccountAnimes.AccountAnimes)
        self.assertIsInstance(self.account.mangas, AccountMangas.AccountMangas)


def main():
    unittest.main()


if '__main__' == __name__:
    main()
