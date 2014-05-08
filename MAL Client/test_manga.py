import unittest
import Manga
import global_functions
from global_functions_for_testing import connection_for_testing
import constants_for_testing


class AnimeTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manga_real_connect = global_functions.connect
        Manga.connect = connection_for_testing
        cls.anime = Manga.Manga(constants_for_testing.MANGA_ID)

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