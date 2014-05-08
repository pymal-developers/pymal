import unittest
from Account import Account
from constants_for_testing import ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD


class AnimeTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.account = Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        cls.animes = cls.account.animes

    def test_animes_len(self):
        self.assertGreater(len(self.animes), 0)


def main():
    unittest.main()


if '__main__' == __name__:
    main()