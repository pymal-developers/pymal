import unittest

from pymal import Account
from pymal import AccountMangas
from pymal import Manga

from tests.constants_for_testing import ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD


class AccountMangaListTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.account = Account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        cls.mangas = cls.account.mangas

    @classmethod
    def tearDownClass(cls):
        AccountMangas.AccountMangas._unregiter(cls.mangas)
        Account.Account._unregiter(cls.account)

    def test_len(self):
        self.assertEquals(len(self.mangas), 1)

    def test_contains_manga(self):
        my_manga = list(self.mangas)[0]
        manga = Manga.Manga(my_manga.id)
        self.assertIn(manga, self.mangas)

    def test_contains_my_manga(self):
        my_manga = list(self.mangas)[0]
        self.assertIn(my_manga, self.mangas)

    def test_contains_id(self):
        my_manga = list(self.mangas)[0]
        self.assertIn(my_manga.id, self.mangas)

    def test_str(self):
        self.assertEqual(str(self.mangas), "<User mangas' number is 1>")


def main():
    unittest.main()


if '__main__' == __name__:
    main()
