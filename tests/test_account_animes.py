import unittest

from pymal import Account
from pymal import Anime

from tests.constants_for_testing import ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD


class AccountAnimeListTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.account = Account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        cls.animes = cls.account.animes

    def test_len(self):
        self.assertGreater(len(self.animes), 0)

    def test_contains(self):
        my_anime = self.animes[0]
        anime = Anime.Anime(my_anime.id)
        self.assertIn(anime, self.animes)

    def test_str(self):
        repr(self.animes)


def main():
    unittest.main()


if '__main__' == __name__:
    main()
