import unittest
from pymal.Account import Account
from tests.constants_for_testing import ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD


class AccountMangaListTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.account = Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        cls.mangas = cls.account.mangas

    def test_animes_len(self):
        self.assertGreater(len(self.mangas), 0)


def main():
    unittest.main()


if '__main__' == __name__:
    main()