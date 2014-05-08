import unittest
import Account
import constants_for_testing


class AccountInitTestCase(unittest.TestCase):
    def test_account_init_not_auth(self):
        account = Account.Account(constants_for_testing.ACCOUNT_TEST_USERNAME)
        self.assertFalse(account.is_auth)

    def test_account_init_auth(self):
        account = Account.Account(constants_for_testing.ACCOUNT_TEST_USERNAME, constants_for_testing.ACCOUNT_TEST_PASSWORD)
        self.assertTrue(account.is_auth)

    def test_account_init_auth_bad_password(self):
        account = Account.Account(constants_for_testing.ACCOUNT_TEST_USERNAME, constants_for_testing.ACCOUNT_TEST_PASSWORD * 2)
        self.assertFalse(account.is_auth)

    def test_account_init_later_auth(self):
        account = Account.Account(constants_for_testing.ACCOUNT_TEST_USERNAME)
        self.assertFalse(account.is_auth)

        account.change_password(constants_for_testing.ACCOUNT_TEST_PASSWORD)
        self.assertTrue(account.is_auth)


class AccountFunctionsTestCase(unittest.TestCase):
    def setUp(self):
        self.account = Account.Account(constants_for_testing.ACCOUNT_TEST_USERNAME, constants_for_testing.ACCOUNT_TEST_PASSWORD)

    def test_reload(self):
        import IPython
        IPython.embed()
        print(type(self.account.animes))


def main():
    unittest.main()


if '__main__' == __name__:
    main()