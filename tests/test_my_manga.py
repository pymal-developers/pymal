import unittest
from pymal.Account import Account
from tests.constants_for_testing import ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD


class MyMangaTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.account = Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        cls.manga = cls.account.mangas[0]

    def test_my_manga(self):
        self.manga.my_score

def main():
    unittest.main()


if '__main__' == __name__:
    main()
