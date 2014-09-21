import unittest

from pymal import anime
from pymal import seasons
from pymal.inner_objects import season


class TestCase(unittest.TestCase):

    def setUp(self):
        self.seasons = seasons.Seasons()

    def test_seasons(self):
        self.assertIsInstance(self.seasons.seasons, frozenset)

        for ssn in self.seasons.seasons:
            self.assertIsInstance(ssn, season.Season)

    def test_seasons_animes(self):
        ssn = list(self.seasons.seasons)[0]
        self.assertIsInstance(ssn.animes, frozenset)

        for anm in ssn.animes:
            self.assertIsInstance(anm, anime.Anime)

    def test_seasons_contains(self):
        ssn = list(self.seasons.seasons)[0]
        anime = list(ssn.animes)[0]
        self.assertIn(anime, self.seasons)

    def test_season_contains(self):
        ssn = list(self.seasons.seasons)[0]
        anime = list(ssn.animes)[0]
        self.assertIn(anime, ssn)

    def test_str(self):
        repr(self.seasons)
        for ssn in self.seasons.seasons:
            repr(ssn)


def main():
    unittest.main()


if '__main__' == __name__:
    main()
