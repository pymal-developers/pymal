import unittest

from pymal import account
from pymal.account_objects import account_mangas
from pymal.account_objects import account_animes
from pymal.account_objects import account_friends

from tests.constants_for_testing import ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD


class InitTestCase(unittest.TestCase):

    def test_init_not_auth(self):
        accnt = account.Account(ACCOUNT_TEST_USERNAME)
        self.assertFalse(accnt.is_auth)
        account.Account._unregiter(accnt)

    def test_account_init_auth(self):
        accnt = account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        self.assertTrue(accnt.is_auth)
        account.Account._unregiter(accnt)

    def test_init_auth_bad_password(self):
        accnt = account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD * 2)
        self.assertFalse(accnt.is_auth)
        account.Account._unregiter(accnt)

    def test_init_later_auth(self):
        accnt = account.Account(ACCOUNT_TEST_USERNAME)
        self.assertFalse(accnt.is_auth)

        account.change_password(ACCOUNT_TEST_PASSWORD)
        self.assertTrue(accnt.is_auth)
        account.Account._unregiter(accnt)

    def test_init_later_auth_bad_password(self):
        accnt = account.Account(ACCOUNT_TEST_USERNAME)
        self.assertFalse(accnt.is_auth)

        self.assertFalse(accnt.change_password(ACCOUNT_TEST_PASSWORD * 2))
        self.assertFalse(accnt.is_auth)
        account.Account._unregiter(accnt)

    def test_str_no_password(self):
        accnt = account.Account(ACCOUNT_TEST_USERNAME)
        self.assertEqual(str(accnt), "<Account username: pymal-developr>")
        account.Account._unregiter(accnt)

    def test_str_with_password(self):
        accnt = account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        self.assertEqual(str(accnt), "<Account username: pymal-developr>")
        account.Account._unregiter(accnt)

    def test_user_id(self):
        accnt = account.Account(ACCOUNT_TEST_USERNAME)
        self.assertEqual(accnt.user_id, 3854655)
        account.Account._unregiter(accnt)


class FunctionsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.account = account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)

    @classmethod
    def tearDownClass(cls):
        account.Account._unregiter(cls.account)

    def test_reload(self):
        self.assertIsInstance(self.account.animes, account_animes.AccountAnimes)
        self.assertIsInstance(self.account.mangas, account_mangas.AccountMangas)
        self.assertIsInstance(self.account.friends, account_friends.AccountFriends)

    def test_username(self):
        self.assertEqual(self.account.username, ACCOUNT_TEST_USERNAME)


def main():
    unittest.main()


if '__main__' == __name__:
    main()
