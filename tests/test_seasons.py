import unittest

from pymal import Anime
from pymal import Seasons
from pymal import Season


class TestCase(unittest.TestCase):

    def setUp(self):
        self.seasons = Seasons.Seasons()

    def test_seasons(self):
        self.assertIsInstance(self.seasons.seasons, set)

        for season in self.seasons.seasons:
            self.assertIsInstance(season, Season.Season)

    def test_seasons_animes(self):
        season = list(self.seasons.seasons)[0]
        self.assertIsInstance(season.animes, set)

        for anime in season.animes:
            self.assertIsInstance(anime, Anime.Anime)

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
