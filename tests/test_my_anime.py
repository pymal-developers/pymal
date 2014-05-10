import unittest
from pymal.Account import Account
from tests.constants_for_testing import ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD


class MyAnimeTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.account = Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        cls.anime = cls.account.animes[0]

    def test_anime_title(self):
        self.anime.my_score

def main():
    unittest.main()


if '__main__' == __name__:
    main()
