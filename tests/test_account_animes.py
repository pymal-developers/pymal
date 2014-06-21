import unittest

from pymal import Account
from pymal import AccountAnimes
from pymal import Anime
from pymal import MyAnime

from tests.constants_for_testing import ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD, ANIME_ID


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
        anime = Anime.Anime(ANIME_ID)
        self.assertIn(anime, self.animes)

    def test_contains_my_manga(self):
        my_anime = MyAnime.MyAnime(ANIME_ID, 0, self.account)
        self.assertIn(my_anime, self.animes)

    def test_contains_id(self):
        self.assertIn(ANIME_ID, self.animes)

    def test_str(self):
        self.assertEquals(str(self.animes), "<User animes' number is 1>")


class AccountAnimeListInteraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.account = Account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        cls.friend = list(cls.account.friends)[0]
        cls.animes = cls.account.animes
        cls.friend_animes = cls.friend.animes

    @classmethod
    def tearDownClass(cls):
        AccountAnimes.AccountAnimes._unregiter(cls.friend_animes)
        AccountAnimes.AccountAnimes._unregiter(cls.animes)
        Account.Account._unregiter(cls.friend)
        Account.Account._unregiter(cls.account)

    def test_union(self):
        regular = self.animes.union(self.friend_animes)
        operator = self.animes | self.friend_animes
        self.assertEquals(regular, operator)

    def test_intersection(self):
        regular = self.animes.intersection(self.friend_animes)
        operator = self.animes & self.friend_animes
        self.assertEquals(regular, operator)

    def test_difference(self):
        regular = self.animes.difference(self.friend_animes)
        operator = self.animes - self.friend_animes
        self.assertEquals(regular, operator)

    def test_symmetric_difference(self):
        regular = self.animes.symmetric_difference(self.friend_animes)
        operator = self.animes ^ self.friend_animes
        self.assertEquals(regular, operator)

    def test_issubset(self):
        regular = self.animes.issubset(self.friend_animes)
        operator = self.animes <= self.friend_animes
        self.assertEquals(regular, operator)

    def test_issuperset(self):
        regular = self.animes.issubset(self.friend_animes)
        operator = self.animes >= self.friend_animes
        self.assertEquals(regular, operator)


def main():
    unittest.main()


if '__main__' == __name__:
    main()
