import unittest
from Manga import Manga
import global_functions
from global_functions_for_testing import connection_for_testing
from constants_for_testing import MANGA_ID


class AnimeTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manga_real_connect = global_functions.connect
        Manga.connect = connection_for_testing
        cls.anime = Manga(MANGA_ID)

    @classmethod
    def tearDownClass(cls):
        global_functions.connect = cls.manga_real_connect

    def test_manga_title(self):
        self.assertEqual(self.anime.english, 'Lucky â\u02dc\u2020 Star')

    def test_manga_spinoff(self):
        self.assertGreater(len(self.anime.spin_offs), 0 )
        for spin_off in self.anime.spin_offs:
            self.assertEqual(spin_off.__class__, Manga.Manga)


def main():
    unittest.main()


if '__main__' == __name__:
    main()