import unittest
from pymal.Anime import Anime
from tests.constants_for_testing import ANIME_ID


class AnimeTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.anime = Anime(ANIME_ID)

    def test_anime_id(self):
        self.assertIsInstance(self.anime.id, int)
        self.assertEqual(self.anime.id, ANIME_ID)

    def test_anime_title(self):
        self.assertIsInstance(self.anime.english, str)
        self.assertEqual(self.anime.english, 'Lucky☆Star')

    def test_anime_image_url(self):
        self.assertIsInstance(self.anime.image_url, str)

    def test_anime_english(self):
        self.assertIsInstance(self.anime.english, str)

    def test_anime_synonyms(self):
        self.assertIsInstance(self.anime.synonyms, str)

    def test_anime_japanese(self):
        self.assertIsInstance(self.anime.japanese, str)

    def test_anime_type(self):
        self.assertIsInstance(self.anime.type, str)

    def test_anime_episodes(self):
        self.assertIsInstance(self.anime.episodes, int)

    def test_anime_start_time(self):
        self.assertTrue(self.anime.start_time == float('inf') or type(self.anime.start_time) == int)

    def test_anime_end_time(self):
        self.assertTrue(self.anime.end_time == float('inf') or type(self.anime.end_time) == int)


    def test_anime_rating(self):
        self.assertIsInstance(self.anime.rating, int)

    def test_anime_score(self):
        self.assertIsInstance(self.anime.score, float)

    def test_anime_rank(self):
        self.assertIsInstance(self.anime.rank, int)

    def test_anime_popularity(self):
        self.assertIsInstance(self.anime.popularity, int)

    def test_anime_synopsis(self):
        self.assertIsInstance(self.anime.synopsis, str)

    def test_anime_spinoff(self):
        self.assertIsInstance(self.anime.spin_offs, set)
        for spin_off in self.anime.spin_offs:
            self.assertIsInstance(spin_off, Anime)

    def test_anime_adaptations(self):
        self.assertIsInstance(self.anime.adaptations, set)
        for adaptation in self.anime.adaptations:
            self.assertIsInstance(adaptation, Anime)

    def test_anime_characters(self):
        self.assertIsInstance(self.anime.characters, set)
        for character in self.anime.characters:
            self.assertIsInstance(character, str)

    def test_anime_sequals(self):
        self.assertIsInstance(self.anime.sequals, set)
        for sequal in self.anime.sequals:
            self.assertIsInstance(sequal, Anime)

    def test_anime_prequel(self):
        self.assertIsInstance(self.anime.prequel, set)
        for preque in self.anime.prequel:
            self.assertIsInstance(preque, Anime)

    def test_anime_spinoffs(self):
        self.assertIsInstance(self.anime.spin_offs, set)
        for spin_off in self.anime.spin_offs:
            self.assertIsInstance(spin_off, Anime)

    def test_anime_alternative_versions(self):
        self.assertIsInstance(self.anime.alternative_versions, set)
        for alternative_version in self.anime.alternative_versions:
            self.assertIsInstance(alternative_version, Anime)

    def test_anime_side_story(self):
        self.assertIsInstance(self.anime.side_stories, set)
        for side_story in self.anime.side_stories:
            self.assertIsInstance(side_story, Anime)

    def test_anime_summaries(self):
        self.assertIsInstance(self.anime.summaries, set)
        for summary in self.anime.summaries:
            self.assertIsInstance(summary, Anime)

    def test_anime_other(self):
        self.assertIsInstance(self.anime.others, set)
        for other in self.anime.others:
            self.assertIsInstance(other, Anime)

    def test_anime_parent_stories(self):
        self.assertIsInstance(self.anime.parent_stories, set)
        for parent_story in self.anime.parent_stories:
            self.assertIsInstance(parent_story, Anime)

    def test_anime_alternative_settings(self):
        self.assertIsInstance(self.anime.alternative_settings, set)
        for alternative_setting in self.anime.alternative_settings:
            self.assertIsInstance(alternative_setting, Anime)


def main():
    unittest.main()


if '__main__' == __name__:
    main()