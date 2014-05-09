import unittest
from Anime import Anime
from constants_for_testing import ANIME_ID


class AnimeTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.anime = Anime(ANIME_ID)

    def test_anime_title(self):
        self.assertEqual(self.anime.english, 'Lucky☆Star')

    def test_anime_spinoff(self):
        self.assertGreater(len(self.anime.spin_offs), 0 )
        for spin_off in self.anime.spin_offs:
            self.assertEqual(spin_off.__class__, Anime)


def main():
    unittest.main()


if '__main__' == __name__:
    main()