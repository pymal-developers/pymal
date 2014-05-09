import unittest
from Account import Account
from AccountAnimes import AccountAnimes
from constants_for_testing import ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD


class AccountInitTestCase(unittest.TestCase):
    def test_account_init_not_auth(self):
        account = Account(ACCOUNT_TEST_USERNAME)
        self.assertFalse(account.is_auth)

    def test_account_init_auth(self):
        account = Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        self.assertTrue(account.is_auth)

    def test_account_init_auth_bad_password(self):
        account = Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD * 2)
        self.assertFalse(account.is_auth)

    def test_account_init_later_auth(self):
        account = Account(ACCOUNT_TEST_USERNAME)
        self.assertFalse(account.is_auth)

        account.change_password(ACCOUNT_TEST_PASSWORD)
        self.assertTrue(account.is_auth)


class AccountFunctionsTestCase(unittest.TestCase):
    def setUp(self):
        self.account = Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)

    def test_reload(self):
        assert type(self.account.animes) == AccountAnimes


def main():
    unittest.main()


if '__main__' == __name__:
    main()