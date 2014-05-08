import unittest
import Anime
import global_functions
import constants_for_testing
from global_functions_for_testing import connection_for_testing


class AnimeTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.anime_real_connect = global_functions.connect
        Anime.connect = connection_for_testing
        cls.anime = Anime.Anime(constants_for_testing.ANIME_ID)

    @classmethod
    def tearDownClass(cls):
        global_functions.connect = cls.anime_real_connect

    def test_anime_title(self):
        self.assertEqual(self.anime.english, 'Luckyâ\u02dc\u2020Star')

    def test_anime_spinoff(self):
        self.assertGreater(len(self.anime.spin_offs), 0 )
        for spin_off in self.anime.spin_offs:
            self.assertEqual(spin_off.__class__, Anime.Anime)


def main():
    unittest.main()


if '__main__' == __name__:
    main()