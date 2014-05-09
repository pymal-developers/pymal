import unittest
from Anime import Anime
import global_functions
from constants_for_testing import ANIME_ID
from global_functions_for_testing import connection_for_testing


class AnimeTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.anime_real_connect = global_functions.connect
        Anime.connect = connection_for_testing
        cls.anime = Anime(ANIME_ID)

    @classmethod
    def tearDownClass(cls):
        global_functions.connect = cls.anime_real_connect

    def test_anime_title(self):
        self.assertEqual(self.anime.english, 'Lucky\u2606Star')

    def test_anime_spinoff(self):
        self.assertGreater(len(self.anime.spin_offs), 0 )
        for spin_off in self.anime.spin_offs:
            self.assertEqual(spin_off.__class__, Anime)


def main():
    unittest.main()


if '__main__' == __name__:
    main()