import unittest
from pymal.Account import Account
from pymal.Anime import Anime
from pymal.consts import MALAPI_FORMAT_TIME, MALAPI_NONE_TIME
from tests.constants_for_testing import ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD
import time


class MyAnimeReloadTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.account = Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        cls.anime = cls.account.animes[0]
        cls.anime.my_reload()

    def test_my_id(self):
        self.assertIsInstance(self.anime.my_id, int)

    def test_my_status(self):
        self.assertIsInstance(self.anime.my_status, int)

    def test_my_is_rewatching(self):
        self.assertIsInstance(self.anime.my_is_rewatching, bool)

    def test_my_manga_my_completed_episodes(self):
        self.assertIsInstance(self.anime.my_completed_episodes, int

    def test_my_tags(self):
        self.assertIsInstance(self.anime.my_tags, str)

    def test_my_comments(self):
        self.assertIsInstance(self.anime.my_comments, str)

    def test_my_fan_sub_group(self):
        self.assertIsInstance(self.anime.my_fan_sub_group, str)

    def test_my_score(self):
        self.assertIsInstance(self.anime.my_score, int)

    def test_my_start_date(self):
        self.assertIsInstance(self.anime.my_start_date, str)
        try:
            self.assertEqual(self.anime.my_start_date, MALAPI_NONE_TIME)
        except AssertionError:
            time.strptime(self.anime.my_start_date, MALAPI_FORMAT_TIME)

    def test_my_end_date(self):
        self.assertIsInstance(self.anime.my_end_date, str)
        try:
            self.assertEqual(self.anime.my_end_date, MALAPI_NONE_TIME)
        except AssertionError:
            time.strptime(self.anime.my_end_date, MALAPI_FORMAT_TIME)

    def test_my_priority(self):
        self.assertIsInstance(self.anime.my_priority, int)

    def test_my_storage_type(self):
        self.assertIsInstance(self.anime.my_storage_type, int)

    def test_my_storage_value(self):
        self.assertIsInstance(self.anime.my_storage_value, float)

    def test_my_download_episodes(self):
        self.assertIsInstance(self.anime.my_download_episodes, int)

    def test_my_times_rewatched(self):
        self.assertIsInstance(self.anime.my_times_rewatched, int)

    def test_my_rewatch_value(self):
        self.assertIsInstance(self.anime.my_rewatch_value, int)

    def test_to_xml(self):
        from xml.etree import ElementTree
        xml = self.anime.to_xml()
        try:
            ElementTree.fromstring(xml)
        except BaseException as err:
            print(err)
            self.assertTrue(False)


class MyAnimeNoReloadTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.account = Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        cls.anime = cls.account.animes[0]

    def test_my_id(self):
        self.assertIsInstance(self.anime.my_id, int)

    def test_my_status(self):
        self.assertIsInstance(self.anime.my_status, int)

    def test_my_is_rewatching(self):
        self.assertIsInstance(self.anime.my_is_rewatching, bool)

    def test_my_manga_my_completed_episodes(self):
        self.assertIsInstance(self.anime.my_completed_episodes, int)

    def test_my_tags(self):
        self.assertIsInstance(self.anime.my_tags, str)

    def test_my_start_date(self):
        self.assertIsInstance(self.anime.my_start_date, str)
        try:
            self.assertEqual(self.anime.my_start_date, MALAPI_NONE_TIME)
        except AssertionError:
            time.strptime(self.anime.my_start_date, MALAPI_FORMAT_TIME)

    def test_my_end_date(self):
        self.assertIsInstance(self.anime.my_end_date, str)
        try:
            self.assertEqual(self.anime.my_end_date, MALAPI_NONE_TIME)
        except AssertionError:
            time.strptime(self.anime.my_end_date, MALAPI_FORMAT_TIME)

    def test_my_times_rewatched(self):
        self.assertIsInstance(self.anime.my_times_rewatched, int)

    def test_my_rewatch_value(self):
        self.assertIsInstance(self.anime.my_rewatch_value, int)

    def test_equal(self):
        anime = Anime(self.anime.id)
        self.assertEqual(anime, self.anime)


def main():
    unittest.main()


if '__main__' == __name__:
    main()
