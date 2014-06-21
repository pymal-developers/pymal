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
        self.assertEqual(self.anime.id, ANIME_ID)

    def test_title(self):
        self.assertEqual(self.anime.title, 'Lucky☆Star')

    def test_image_url(self):
        self.assertEqual(self.anime.image_url, 'http://cdn.myanimelist.net/images/anime/13/15010.jpg')

    def test_english(self):
        self.assertEqual(self.anime.english, 'Lucky☆Star')

    def test_synonyms(self):
        self.assertEqual(self.anime.synonyms, 'Lucky Star')

    def test_japanese(self):
        self.assertEqual(self.anime.japanese, 'らき☆すた')

    def test_type(self):
        self.assertEqual(self.anime.type, 'TV')

    def test_episodes(self):
        self.assertEqual(self.anime.episodes, 24)
        # need to take something with no number
        #self.assertEqual(self.anime.episodes, float('inf'))

    def test_start_time(self):
        self.assertEqual(self.anime.start_time, 1175979600)

    def test_end_time(self):
        self.assertEqual(self.anime.end_time, 1189976400.0)

    def test_rating(self):
        self.assertEqual(self.anime.rating, 'PG-13 - Teens 13 or older')

    def test_duration(self):
        self.assertEqual(self.anime.duration, 24)

    def test_score(self):
        self.assertIsInstance(self.anime.score, float)

    def test_rank(self):
        self.assertIsInstance(self.anime.rank, int)

    def test_popularity(self):
        self.assertIsInstance(self.anime.popularity, int)

    def test_synopsis(self):
        self.assertEqual(self.anime.synopsis, """Having fun in school, doing homework together, cooking and eating, playing videogames, watching anime. All those little things make up the daily life of the anime—and chocolate-loving—Izumi Konata and her friends. Sometimes relaxing but more than often simply funny!\r\n""")

    def test_spinoff(self):
        self.assertIsInstance(self.anime.spin_offs, frozenset)
        self.assertEqual(len(self.anime.spin_offs), 1)
        for spin_off in self.anime.spin_offs:
            self.assertIsInstance(spin_off, Anime.Anime)
        self.assertIn(17637, list(self.anime.spin_offs))

    def test_adaptations(self):
        self.assertIsInstance(self.anime.adaptations, frozenset)
        self.assertEqual(len(self.anime.adaptations), 1)
        for adaptation in self.anime.adaptations:
            self.assertIsInstance(adaptation, Manga.Manga)
        self.assertIn(587, list(self.anime.adaptations))

    def test_characters(self):
        self.assertIsInstance(self.anime.characters, frozenset)
        self.assertEqual(len(self.anime.characters), 1)
        for character in self.anime.characters:
            self.assertIsInstance(character, Anime.Anime)
        self.assertIn(3080, list(self.anime.characters))

    def test_sequals(self):
        self.assertIsInstance(self.anime.sequels, frozenset)
        self.assertEqual(len(self.anime.sequels), 1)
        for sequal in self.anime.sequels:
            self.assertIsInstance(sequal, Anime.Anime)
        self.assertIn(4472, list(self.anime.sequels))

    def test_prequels(self):
        self.assertIsInstance(self.anime.prequels, frozenset)
        self.assertEqual(len(self.anime.prequels), 0)
        for prequel in self.anime.prequels:
            self.assertIsInstance(prequel, Anime.Anime)

    def test_alternative_versions(self):
        self.assertIsInstance(self.anime.alternative_versions, frozenset)
        self.assertEqual(len(self.anime.alternative_versions), 0)
        for alternative_version in self.anime.alternative_versions:
            self.assertIsInstance(alternative_version, Anime.Anime)

    def test_side_story(self):
        self.assertIsInstance(self.anime.side_stories, frozenset)
        self.assertEqual(len(self.anime.side_stories), 0)
        for side_story in self.anime.side_stories:
            self.assertIsInstance(side_story, Anime.Anime)

    def test_summaries(self):
        self.assertIsInstance(self.anime.summaries, frozenset)
        self.assertEqual(len(self.anime.summaries), 0)
        for summary in self.anime.summaries:
            self.assertIsInstance(summary, Anime.Anime)

    def test_other(self):
        self.assertIsInstance(self.anime.others, frozenset)
        self.assertEqual(len(self.anime.others), 0)
        for other in self.anime.others:
            self.assertIsInstance(other, Anime.Anime)

    def test_parent_stories(self):
        self.assertIsInstance(self.anime.parent_stories, frozenset)
        self.assertEqual(len(self.anime.parent_stories), 0)
        for parent_story in self.anime.parent_stories:
            self.assertIsInstance(parent_story, Anime.Anime)

    def test_alternative_settings(self):
        self.assertIsInstance(self.anime.alternative_settings, frozenset)
        self.assertEqual(len(self.anime.alternative_settings), 0)
        for alternative_setting in self.anime.alternative_settings:
            self.assertIsInstance(alternative_setting, Anime.Anime)

    def test_full_stories(self):
        self.assertIsInstance(self.anime.full_stories, frozenset)
        self.assertEqual(len(self.anime.full_stories), 0)
        for full_story in self.anime.full_stories:
            self.assertIsInstance(full_story, Anime.Anime)

    def test_str(self):
        self.assertEqual(str(self.anime), "<Anime Lucky☆Star id=1887>")


class NoReloadTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.account = Account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        cls.anime = list(cls.account.animes)[0]

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

    def test_str(self):
        repr(self.anime)

    def test_add_and_delete(self):
        from pymal import MyAnime
        anime = Anime.Anime(20707)
        my_anime = anime.add(self.account)
        try:
            self.assertIsInstance(my_anime, MyAnime.MyAnime)
            self.account.animes.reload()
            self.assertIn(my_anime, self.account.animes)
        finally:
            my_anime.delete()

        self.account.animes.reload()
        self.assertNotIn(my_anime, self.account.animes)


def main():
    unittest.main()


if '__main__' == __name__:
    main()
