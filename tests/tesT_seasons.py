import unittest

from pymal import anime
from pymal import seasons
from pymal.inner_objects import season


class TestCase(unittest.TestCase):

    def setUp(self):
        self.seasons = seasons.Seasons()

    def test_seasons(self):
        self.assertIsInstance(self.seasons.seasons, frozenset)

        for season in self.seasons.seasons:
            self.assertIsInstance(season, season.Season)

    def test_seasons_animes(self):
        ssn = list(self.seasons.seasons)[0]
        self.assertIsInstance(ssn.animes, frozenset)

        for anime in ssn.animes:
            self.assertIsInstance(anime, anime.Anime)

    def test_seasons_contains(self):
        season = list(self.seasons.seasons)[0]
        anime = list(season.animes)[0]
        self.assertIn(anime, self.seasons)

    def test_season_contains(self):
        season = list(self.seasons.seasons)[0]
        anime = list(season.animes)[0]
        self.assertIn(anime, season)

    def test_str(self):
        repr(self.seasons)
        for season in self.seasons.seasons:
            repr(season)


def main():
    unittest.main()


if '__main__' == __name__:
    main()
