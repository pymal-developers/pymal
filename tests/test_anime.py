import unittest

from pymal import Account
from pymal import Anime
from pymal import Manga

from tests.constants_for_testing import ANIME_ID, ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD


class ReloadTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.anime = Anime.Anime(ANIME_ID)
        cls.anime.reload()

    def test_id(self):
        self.assertIsInstance(self.anime.id, int)
        self.assertEqual(self.anime.id, ANIME_ID)

    def test_title(self):
        self.assertIsInstance(self.anime.english, str)
        self.assertEqual(self.anime.english, 'Lucky☆Star')

    def test_image_url(self):
        self.assertIsInstance(self.anime.image_url, str)

    def test_english(self):
        self.assertIsInstance(self.anime.english, str)

    def test_synonyms(self):
        self.assertIsInstance(self.anime.synonyms, str)

    def test_japanese(self):
        self.assertIsInstance(self.anime.japanese, str)

    def test_type(self):
        self.assertIsInstance(self.anime.type, str)

    def test_episodes(self):
        try:
            self.assertIsInstance(self.anime.episodes, int)
        except AssertionError:
            self.assertEqual(self.anime.episodes, float('inf'))

    def test_start_time(self):
        self.assertIsInstance(self.anime.start_time, float)

    def test_end_time(self):
        self.assertIsInstance(self.anime.end_time, float)

    def test_rating(self):
        self.assertIsInstance(self.anime.rating, str)

    def test_score(self):
        self.assertIsInstance(self.anime.score, float)

    def test_rank(self):
        self.assertIsInstance(self.anime.rank, int)

    def test_popularity(self):
        self.assertIsInstance(self.anime.popularity, int)

    def test_synopsis(self):
        self.assertIsInstance(self.anime.synopsis, str)

    def test_spinoff(self):
        self.assertIsInstance(self.anime.spin_offs, list)
        for spin_off in self.anime.spin_offs:
            self.assertIsInstance(spin_off, Anime.Anime)

    def test_adaptations(self):
        self.assertIsInstance(self.anime.adaptations, list)
        for adaptation in self.anime.adaptations:
            self.assertIsInstance(adaptation, Manga.Manga)

    def test_characters(self):
        self.assertIsInstance(self.anime.characters, list)
        for character in self.anime.characters:
            self.assertIsInstance(character, Anime.Anime)

    def test_sequals(self):
        self.assertIsInstance(self.anime.sequels, list)
        for sequal in self.anime.sequels:
            self.assertIsInstance(sequal, Anime.Anime)

    def test_prequels(self):
        self.assertIsInstance(self.anime.prequels, list)
        for prequel in self.anime.prequels:
            self.assertIsInstance(prequel, Anime.Anime)

    def test_alternative_versions(self):
        self.assertIsInstance(self.anime.alternative_versions, list)
        for alternative_version in self.anime.alternative_versions:
            self.assertIsInstance(alternative_version, Anime.Anime)

    def test_side_story(self):
        self.assertIsInstance(self.anime.side_stories, list)
        for side_story in self.anime.side_stories:
            self.assertIsInstance(side_story, Anime.Anime)

    def test_summaries(self):
        self.assertIsInstance(self.anime.summaries, list)
        for summary in self.anime.summaries:
            self.assertIsInstance(summary, Anime.Anime)

    def test_other(self):
        self.assertIsInstance(self.anime.others, list)
        for other in self.anime.others:
            self.assertIsInstance(other, Anime.Anime)

    def test_parent_stories(self):
        self.assertIsInstance(self.anime.parent_stories, list)
        for parent_story in self.anime.parent_stories:
            self.assertIsInstance(parent_story, Anime.Anime)

    def test_alternative_settings(self):
        self.assertIsInstance(self.anime.alternative_settings, list)
        for alternative_setting in self.anime.alternative_settings:
            self.assertIsInstance(alternative_setting, Anime.Anime)

    def test_full_stories(self):
        self.assertIsInstance(self.anime.full_stories, list)
        for full_story in self.anime.full_stories:
            self.assertIsInstance(full_story, Anime.Anime)


class NoReloadTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.account = Account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        cls.anime = cls.account.animes[0]

    def test_id(self):
        self.assertIsInstance(self.anime.id, int)

    def test_title(self):
        self.assertIsInstance(self.anime.english, str)

    def test_image_url(self):
        self.assertIsInstance(self.anime.image_url, str)

    def test_synonyms(self):
        self.assertIsInstance(self.anime.synonyms, str)

    def test_type(self):
        self.assertIsInstance(self.anime.type, str)

    def test_episodes(self):
        try:
            self.assertIsInstance(self.anime.episodes, int)
        except AssertionError:
            self.assertEqual(self.anime.episodes, float('inf'))

    def test_start_time(self):
        self.assertIsInstance(self.anime.start_time, float)

    def test_end_time(self):
        self.assertIsInstance(self.anime.end_time, float)


def main():
    unittest.main()


if '__main__' == __name__:
    main()
