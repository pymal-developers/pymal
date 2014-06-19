import unittest

from pymal import Account
from pymal import AccountAnimes
from pymal import Anime

from tests.constants_for_testing import ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD


class AccountAnimeListTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.account = Account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        cls.animes = cls.account.animes

    @classmethod
    def tearDownClass(cls):
        AccountAnimes.AccountAnimes._unregiter(cls.animes)
        Account.Account._unregiter(cls.account)

    def test_len(self):
        self.assertEquals(len(self.animes), 1)

    def test_contains(self):
        my_anime = list(self.animes)[0]
        anime = Anime.Anime(my_anime.id)
        self.assertIn(anime, self.animes)

    def test_contains_my_manga(self):
        my_anime = list(self.animes)[0]
        self.assertIn(my_anime, self.animes)

    def test_contains_id(self):
        my_anime = list(self.animes)[0]
        self.assertIn(my_anime.id, self.animes)

    def test_str(self):
        self.assertEquals(str(self.animes), "<User animes' number is 0>")


def main():
    unittest.main()


if '__main__' == __name__:
    main()
