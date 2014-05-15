import unittest
from pymal.Account import Account
from tests.constants_for_testing import ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD


class MyAnimeTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.account = Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        cls.anime = cls.account.animes[0]

    def test_my_anime_my_id(self):
        self.assertIsInstance(self.anime.my_id, int)

    def test_my_anime_my_status(self):
        self.assertIsInstance(self.anime.my_status, int)

    def test_my_anime_my_is_rewatching(self):
        self.assertIsInstance(self.anime.my_is_rewatching, bool)

    def test_my_manga_my_completed_episodes(self):
        self.assertIsInstance(self.anime.my_completed_episodes, int)

    def test_my_anime_my_score(self):
        self.assertIsInstance(self.anime.my_score, int)

    def test_my_anime_my_start_date(self):
        self.assertTrue(self.anime.my_start_date == float('inf') or type(self.anime.my_start_date) == int)

    def test_my_anime_my_end_date(self):
        self.assertTrue(self.anime.my_end_date == float('inf') or type(self.anime.my_end_date) == int)

    def test_my_anime_my_priority(self):
        self.assertIsInstance(self.anime.my_priority, int)

    def test_my_anime_my_storage_type(self):
        self.assertIsInstance(self.anime.my_storage_type, int)

    def test_my_anime_my_storage_value(self):
        self.assertIsInstance(self.anime.my_storage_value, int)

    def test_my_anime_my_download_episodes(self):
        self.assertIsInstance(self.anime.my_download_episodes, int)

    def test_my_anime_my_times_rewatched(self):
        self.assertIsInstance(self.anime.my_times_rewatched, int)

    def test_my_anime_my_rewatch_value(self):
        self.assertIsInstance(self.anime.my_rewatch_value, int)


def main():
    unittest.main()


if '__main__' == __name__:
    main()
