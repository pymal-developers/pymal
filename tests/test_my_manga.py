import unittest
from pymal.Account import Account
from pymal.consts import MALAPI_FORMAT_TIME, MALAPI_NONE_TIME
from tests.constants_for_testing import ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD
import time


class MyMangaTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.account = Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        cls.manga = cls.account.mangas[0]
        cls.manga.my_reload()

    def test_my_manga_my_id(self):
        self.assertIsInstance(self.manga.my_id, int)

    def test_my_manga_my_status(self):
        self.assertIsInstance(self.manga.my_status, int)

    def test_my_manga_my_is_rereading(self):
        self.assertIsInstance(self.manga.my_is_rereading, bool)

    def test_my_manga_my_completed_chapters(self):
        self.assertIsInstance(self.manga.my_completed_chapters, int)

    def test_my_manga_my_completed_volumes(self):
        self.assertIsInstance(self.manga.my_completed_volumes, int)

    def test_my_manga_my_score(self):
        self.assertIsInstance(self.manga.my_start_date, str)
        try:
            self.assertEqual(self.manga.my_start_date, MALAPI_NONE_TIME)
        except AssertionError:
            time.strptime(self.manga.my_start_date, MALAPI_FORMAT_TIME)

    def test_my_manga_my_start_date(self):
        self.assertIsInstance(self.manga.my_end_date, str)
        try:
            self.assertEqual(self.manga.my_end_date, MALAPI_NONE_TIME)
        except AssertionError:
            time.strptime(self.manga.my_end_date, MALAPI_FORMAT_TIME)

    def test_my_manga_my_end_date(self):
        self.assertTrue(self.manga.my_end_date == float('inf') or type(self.manga.my_end_date) == int)

    def test_my_manga_my_priority(self):
        self.assertIsInstance(self.manga.my_priority, int)

    def test_my_manga_my_storage_type(self):
        self.assertIsInstance(self.manga.my_storage_type, int)

    def test_my_manga_my_storage_value(self):
        self.assertIsInstance(self.manga.my_storage_value, int)

    def test_my_manga_my_download_episodes(self):
        self.assertIsInstance(self.manga.my_download_episodes, int)

    def test_my_manga_my_times_reread(self):
        self.assertIsInstance(self.manga.my_times_reread, int)

    def test_my_manga_my_reread_value(self):
        self.assertIsInstance(self.manga.my_reread_value, int)

def main():
    unittest.main()


if '__main__' == __name__:
    main()
