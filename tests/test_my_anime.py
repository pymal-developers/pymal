import unittest
import time
from xml.etree import ElementTree

from pymal import Account
from pymal import Anime
from pymal import consts

from tests.constants_for_testing import ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD


class ReloadTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.account = Account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        cls.anime = list(cls.account.animes)[0]
        cls.anime.my_reload()

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

    def test_my_comments(self):
        self.assertIsInstance(self.anime.my_comments, str)

    def test_my_fan_sub_groups(self):
        self.assertIsInstance(self.anime.my_fan_sub_groups, str)

    def test_my_score(self):
        self.assertIsInstance(self.anime.my_score, int)

    def test_my_start_date(self):
        self.assertIsInstance(self.anime.my_start_date, str)
        try:
            self.assertEqual(self.anime.my_start_date, consts.MALAPI_NONE_TIME)
        except AssertionError:
            time.strptime(self.anime.my_start_date, consts.MALAPI_FORMAT_TIME)

    def test_my_end_date(self):
        self.assertIsInstance(self.anime.my_end_date, str)
        try:
            self.assertEqual(self.anime.my_end_date, consts.MALAPI_NONE_TIME)
        except AssertionError:
            time.strptime(self.anime.my_end_date, consts.MALAPI_FORMAT_TIME)

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
        xml = self.anime.to_xml()
        try:
            ElementTree.fromstring(xml)
        except BaseException as err:
            print(err)
            self.assertTrue(False)

    def test_str(self):
        repr(self.anime)

    def test_update(self):
        self.anime.update()


class NoReloadTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.account = Account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        cls.anime = list(cls.account.animes)[0]

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
            self.assertEqual(self.anime.my_start_date, consts.MALAPI_NONE_TIME)
        except AssertionError:
            time.strptime(self.anime.my_start_date, consts.MALAPI_FORMAT_TIME)

    def test_my_end_date(self):
        self.assertIsInstance(self.anime.my_end_date, str)
        try:
            self.assertEqual(self.anime.my_end_date, consts.MALAPI_NONE_TIME)
        except AssertionError:
            time.strptime(self.anime.my_end_date, consts.MALAPI_FORMAT_TIME)

    def test_my_times_rewatched(self):
        self.assertIsInstance(self.anime.my_times_rewatched, int)

    def test_my_rewatch_value(self):
        self.assertIsInstance(self.anime.my_rewatch_value, int)

    def test_equal(self):
        anime = Anime.Anime(self.anime.id)
        self.assertEqual(anime, self.anime)

    def test_str(self):
        repr(self.anime)


def main():
    unittest.main()


if '__main__' == __name__:
    main()
