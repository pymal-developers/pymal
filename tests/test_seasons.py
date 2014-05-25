import unittest

from pymal.Anime import Anime
from pymal.Seasons import Seasons
from pymal.Season import Season


class TestCase(unittest.TestCase):
    def setUp(self):
        self.seasons = Seasons()

    def test_seasons(self):
        self.assertIsInstance(self.seasons.seasons, set)

        for season in self.seasons.seasons:
            self.assertIsInstance(season, Season)

    def test_seasons_animes(self):
        season = list(self.seasons.seasons)[0]
        self.assertIsInstance(season.animes, set)

        for anime in season.animes:
            self.assertIsInstance(anime, Anime)

    def test_seasons_contains(self):
        season = list(self.seasons.seasons)[0]
        anime = list(season.animes)[0]
        self.assertIn(anime, self.seasons)

    def test_season_contains(self):
        season = list(self.seasons.seasons)[0]
        anime = list(season.animes)[0]
        self.assertIn(anime, season)


def main():
    unittest.main()


if '__main__' == __name__:
    main()