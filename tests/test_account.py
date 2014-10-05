import unittest
from mock import Mock

import bs4
from os import path

from pymal import account
from pymal.account_objects import account_mangas
from pymal.account_objects import account_animes
from pymal.account_objects import account_friends
from pymal import global_functions

from tests.constants_for_testing import ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD, SOURCES_DIRECTORY


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

        accnt.change_password(ACCOUNT_TEST_PASSWORD)
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


class NoReloadFunctionsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.account = account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        cls._reload = cls.account.reload
        cls.account.reload = Mock(wraps=cls._reload)

    @classmethod
    def tearDownClass(cls):
        cls.account.reload = cls._reload
        account.Account._unregiter(cls.account)

    def tearDown(self):
        self.assertFalse(self.account.reload.called)

    def test_animes(self):
        self.assertIsInstance(self.account.animes, account_animes.AccountAnimes)

    def test_mangas(self):
        self.assertIsInstance(self.account.mangas, account_mangas.AccountMangas)

    def test_friends(self):
        self.assertIsInstance(self.account.friends, account_friends.AccountFriends)

    def test_username(self):
        self.assertEqual(self.account.username, ACCOUNT_TEST_USERNAME)


class ReloadFunctionsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.account = account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        cls._reload = cls.account.reload

        cls.__get_content_wrapper_div = global_functions.get_content_wrapper_div

        with open(path.join(SOURCES_DIRECTORY, "pymal-developr's Profile - MyAnimeList.net.html"), "rb") as f:
            data = f.read().decode()
        html = bs4.BeautifulSoup(data, "html5lib")
        myanimelist_div = html.body.find(name="div", attrs={"id": 'myanimelist'})
        content_wrapper_div = myanimelist_div.find(name="div", attrs={"id": "contentWrapper"}, recursive=False)

        global_functions.get_content_wrapper_div = Mock(return_value=content_wrapper_div)

        cls.account.reload = Mock(wraps=cls._reload)

    @classmethod
    def tearDownClass(cls):
        cls.account.reload = cls._reload
        global_functions.get_content_wrapper_div = cls.__get_content_wrapper_div
        account.Account._unregiter(cls.account)

    def tearDown(self):
        self.account.reload.assert_called_once_with()
        global_functions.get_content_wrapper_div.assert_called_once_with(
            self.account._main_profile_url,
            global_functions.connect
        )

    def test_image_url(self):
        self.assertEqual(self.account.image_url, "pymal-developr%27s%20Profile%20-%20MyAnimeList.net_files/na.gif")


def main():
    unittest.main()


if '__main__' == __name__:
    main()
