import unittest
from unittest.mock import Mock
import os
from os import path

from pymal import account
from pymal import anime
from pymal import manga
from pymal import global_functions
from pymal.account_objects import my_anime
import bs4

from tests.constants_for_testing import ADD_ANIME_ID, ANIME_ID, ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD,\
    SOURCES_DIRECTORY


class ReloadTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.anime = anime.Anime(ANIME_ID)
        cls.__global_functions_get_content_wrapper_div = global_functions.get_content_wrapper_div

        with open(path.join(SOURCES_DIRECTORY, "Lucky☆Star - MyAnimeList.net.html"), "rb") as f:
            data = f.read().decode()
        html = bs4.BeautifulSoup(data, "html5lib")
        myanimelist_div = html.body.find(name="div", attrs={"id": 'myanimelist'})
        content_wrapper_div = myanimelist_div.find(name="div", attrs={"id": "contentWrapper"}, recursive=False)
        global_functions.get_content_wrapper_div = Mock(return_value=content_wrapper_div)

        cls.anime.reload()

    @classmethod
    def tearDownClass(cls):
        global_functions.get_content_wrapper_div = cls.__global_functions_get_content_wrapper_div

    def test_id(self):
        self.assertEqual(self.anime.id, ANIME_ID)

    def test_title(self):
        self.assertEqual(self.anime.title, 'Lucky☆Star')

    def test_image_url(self):
        self.assertEqual(self.anime.image_url, 'Lucky%E2%98%86Star%20-%20MyAnimeList.net_files/15010.jpg')

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
        self.assertEqual(self.anime.start_time, 1175990400)

    def test_end_time(self):
        self.assertEqual(self.anime.end_time, 1189987200)

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
        self.assertEqual(self.anime.synopsis, "Having fun in school, doing homework \ntogether, cooking and eating, playing videogames, watching anime. All \nthose little things make up the daily life of the anime—and \nchocolate-loving—Izumi Konata and her friends. Sometimes relaxing but \nmore than often simply funny!" + os.linesep)

    def test_spinoff(self):
        self.assertIsInstance(self.anime.spin_offs, frozenset)
        self.assertEqual(len(self.anime.spin_offs), 1)
        for spin_off in self.anime.spin_offs:
            self.assertIsInstance(spin_off, anime.Anime)
        self.assertIn(17637, list(self.anime.spin_offs))

    def test_adaptations(self):
        self.assertIsInstance(self.anime.adaptations, frozenset)
        self.assertEqual(len(self.anime.adaptations), 1)
        for adaptation in self.anime.adaptations:
            self.assertIsInstance(adaptation, manga.Manga)
            self.assertIsInstance(adaptation, manga.Manga)
        self.assertIn(587, list(self.anime.adaptations))

    def test_characters(self):
        self.assertIsInstance(self.anime.characters, frozenset)
        self.assertEqual(len(self.anime.characters), 1)
        for character in self.anime.characters:
            self.assertIsInstance(character, anime.Anime)
        self.assertIn(3080, list(self.anime.characters))

    def test_sequals(self):
        self.assertIsInstance(self.anime.sequels, frozenset)
        self.assertEqual(len(self.anime.sequels), 1)
        for sequal in self.anime.sequels:
            self.assertIsInstance(sequal, anime.Anime)
        self.assertIn(4472, list(self.anime.sequels))

    def test_prequels(self):
        self.assertIsInstance(self.anime.prequels, frozenset)
        self.assertEqual(len(self.anime.prequels), 0)
        for prequel in self.anime.prequels:
            self.assertIsInstance(prequel, anime.Anime)

    def test_alternative_versions(self):
        self.assertIsInstance(self.anime.alternative_versions, frozenset)
        self.assertEqual(len(self.anime.alternative_versions), 0)
        for alternative_version in self.anime.alternative_versions:
            self.assertIsInstance(alternative_version, anime.Anime)

    def test_side_story(self):
        self.assertIsInstance(self.anime.side_stories, frozenset)
        self.assertEqual(len(self.anime.side_stories), 0)
        for side_story in self.anime.side_stories:
            self.assertIsInstance(side_story, anime.Anime)

    def test_summaries(self):
        self.assertIsInstance(self.anime.summaries, frozenset)
        self.assertEqual(len(self.anime.summaries), 0)
        for summary in self.anime.summaries:
            self.assertIsInstance(summary, anime.Anime)

    def test_other(self):
        self.assertIsInstance(self.anime.others, frozenset)
        self.assertEqual(len(self.anime.others), 0)
        for other in self.anime.others:
            self.assertIsInstance(other, anime.Anime)

    def test_parent_stories(self):
        self.assertIsInstance(self.anime.parent_stories, frozenset)
        self.assertEqual(len(self.anime.parent_stories), 0)
        for parent_story in self.anime.parent_stories:
            self.assertIsInstance(parent_story, anime.Anime)

    def test_alternative_settings(self):
        self.assertIsInstance(self.anime.alternative_settings, frozenset)
        self.assertEqual(len(self.anime.alternative_settings), 0)
        for alternative_setting in self.anime.alternative_settings:
            self.assertIsInstance(alternative_setting, anime.Anime)

    def test_full_stories(self):
        self.assertIsInstance(self.anime.full_stories, frozenset)
        self.assertEqual(len(self.anime.full_stories), 0)
        for full_story in self.anime.full_stories:
            self.assertIsInstance(full_story, anime.Anime)

    def test_str(self):
        self.assertEqual(str(self.anime), "<Anime Lucky☆Star id=1887>")


class NoReloadTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.account = account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
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

    @unittest.skip("Delete is not working")
    def test_add_and_delete(self):
        anm = anime.Anime(ADD_ANIME_ID)
        my_anm = anm.add(self.account)

        self.assertIsInstance(my_anm, my_anime.MyAnime)
        self.account.animes.reload()
        self.assertIn(my_anm, self.account.animes)

        my_anm.delete()
        self.account.animes.reload()
        self.assertNotIn(my_anm, self.account.animes)


def main():
    unittest.main()


if '__main__' == __name__:
    main()
