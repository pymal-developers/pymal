import unittest

from pymal import Account
from pymal import Manga

from tests.constants_for_testing import ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD


class AccountMangaListTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.account = Account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        cls.mangas = cls.account.mangas

    def test_len(self):
        self.assertGreater(len(self.mangas), 0)

    def test_contains(self):
        my_manga = self.mangas[0]
        manga = Manga.Manga(my_manga.id)
        self.assertIn(manga, self.mangas)


def main():
    unittest.main()


if '__main__' == __name__:
    main()
