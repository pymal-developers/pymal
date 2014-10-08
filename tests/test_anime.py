import unittest
from mock import Mock
import os
from os import path

import bs4
from pymal.account import Account
from pymal.anime import Anime
from pymal.manga import Manga
from pymal import global_functions
from pymal.account_objects.my_anime import MyAnime

from tests.constants_for_testing import ADD_ANIME_ID, ANIME_ID, ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD,\
    SOURCES_DIRECTORY


class FetchWebTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tested_object = Anime(ANIME_ID)

    def test_fetch_web(self):
        self.tested_object.reload()


class ReloadTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.__global_functions_get_content_wrapper_div = global_functions.get_content_wrapper_div

        with open(path.join(SOURCES_DIRECTORY, "Lucky☆Star - MyAnimeList.net.html"), "rb") as f:
            data = f.read().decode()
        html = bs4.BeautifulSoup(data, "html5lib")
        myanimelist_div = html.body.find(name="div", attrs={"id": 'myanimelist'})
        content_wrapper_div = myanimelist_div.find(name="div", attrs={"id": "contentWrapper"}, recursive=False)
        global_functions.get_content_wrapper_div = Mock(return_value=content_wrapper_div)

    def setUp(self):
        self.tested_object = Anime(ANIME_ID)
        self.__reload = self.tested_object.reload
        self.tested_object.reload = Mock(wraps=self.__reload)

    @classmethod
    def tearDownClass(cls):
        global_functions.get_content_wrapper_div = cls.__global_functions_get_content_wrapper_div

    def tearDown(self):
        self.tested_object.reload.assert_called_once_with()
        Anime._unregiter(self.tested_object)

    def test_title(self):
        self.assertEqual(self.tested_object.title, 'Lucky☆Star')

    def test_image_url(self):
        self.assertEqual(self.tested_object.image_url, 'Lucky%E2%98%86Star%20-%20MyAnimeList.net_files/15010.jpg')

    def test_english(self):
        self.assertEqual(self.tested_object.english, 'Lucky☆Star')

    def test_synonyms(self):
        self.assertEqual(self.tested_object.synonyms, 'Lucky Star')

    def test_japanese(self):
        self.assertEqual(self.tested_object.japanese, 'らき☆すた')

    def test_type(self):
        self.assertEqual(self.tested_object.type, 'TV')

    def test_status(self):
        self.assertEqual(self.tested_object.status, 'Finished Airing')

    def test_episodes(self):
        self.assertEqual(self.tested_object.episodes, 24)
        # TODO: need to take something with no number
        # self.assertEqual(self.tested_object.episodes, float('inf'))

    def test_start_time(self):
        self.assertEqual(self.tested_object.start_time, 1175990400)

    def test_end_time(self):
        self.assertEqual(self.tested_object.end_time, 1189987200)

    def test_rating(self):
        self.assertEqual(self.tested_object.rating, 'PG-13 - Teens 13 or older')

    def test_duration(self):
        self.assertEqual(self.tested_object.duration, 24)

    def test_creators(self):
        self.assertIsInstance(self.tested_object.creators, dict)

    def test_genres(self):
        self.assertIsInstance(self.tested_object.genres, dict)

    def test_score(self):
        self.assertIsInstance(self.tested_object.score, float)

    def test_rank(self):
        self.assertIsInstance(self.tested_object.rank, int)

    def test_popularity(self):
        self.assertIsInstance(self.tested_object.popularity, int)

    def test_synopsis(self):
        self.assertEqual(self.tested_object.synopsis, "Having fun in school, doing homework \ntogether, cooking and eating, playing videogames, watching anime. All \nthose little things make up the daily life of the anime—and \nchocolate-loving—Izumi Konata and her friends. Sometimes relaxing but \nmore than often simply funny!" + os.linesep)

    def test_spinoff(self):
        self.assertIsInstance(self.tested_object.spin_offs, frozenset)
        self.assertEqual(len(self.tested_object.spin_offs), 1)
        for spin_off in self.tested_object.spin_offs:
            self.assertIsInstance(spin_off, Anime)
        self.assertIn(17637, list(self.tested_object.spin_offs))

    def test_adaptations(self):
        self.assertIsInstance(self.tested_object.adaptations, frozenset)
        self.assertEqual(len(self.tested_object.adaptations), 1)
        for adaptation in self.tested_object.adaptations:
            self.assertIsInstance(adaptation, Manga)
        self.assertIn(587, list(self.tested_object.adaptations))

    def test_characters(self):
        self.assertIsInstance(self.tested_object.characters, frozenset)
        self.assertEqual(len(self.tested_object.characters), 1)
        for character in self.tested_object.characters:
            self.assertIsInstance(character, Anime)
        self.assertIn(3080, list(self.tested_object.characters))

    def test_sequals(self):
        self.assertIsInstance(self.tested_object.sequels, frozenset)
        self.assertEqual(len(self.tested_object.sequels), 1)
        for sequal in self.tested_object.sequels:
            self.assertIsInstance(sequal, Anime)
        self.assertIn(4472, list(self.tested_object.sequels))

    def test_prequels(self):
        self.assertIsInstance(self.tested_object.prequels, frozenset)
        self.assertEqual(len(self.tested_object.prequels), 0)
        for prequel in self.tested_object.prequels:
            self.assertIsInstance(prequel, Anime)

    def test_alternative_versions(self):
        self.assertIsInstance(self.tested_object.alternative_versions, frozenset)
        self.assertEqual(len(self.tested_object.alternative_versions), 0)
        for alternative_version in self.tested_object.alternative_versions:
            self.assertIsInstance(alternative_version, Anime)

    def test_side_story(self):
        self.assertIsInstance(self.tested_object.side_stories, frozenset)
        self.assertEqual(len(self.tested_object.side_stories), 0)
        for side_story in self.tested_object.side_stories:
            self.assertIsInstance(side_story, Anime)

    def test_summaries(self):
        self.assertIsInstance(self.tested_object.summaries, frozenset)
        self.assertEqual(len(self.tested_object.summaries), 0)
        for summary in self.tested_object.summaries:
            self.assertIsInstance(summary, Anime)

    def test_other(self):
        self.assertIsInstance(self.tested_object.others, frozenset)
        self.assertEqual(len(self.tested_object.others), 0)
        for other in self.tested_object.others:
            self.assertIsInstance(other, Anime)

    def test_parent_stories(self):
        self.assertIsInstance(self.tested_object.parent_stories, frozenset)
        self.assertEqual(len(self.tested_object.parent_stories), 0)
        for parent_story in self.tested_object.parent_stories:
            self.assertIsInstance(parent_story, Anime)

    def test_alternative_settings(self):
        self.assertIsInstance(self.tested_object.alternative_settings, frozenset)
        self.assertEqual(len(self.tested_object.alternative_settings), 0)
        for alternative_setting in self.tested_object.alternative_settings:
            self.assertIsInstance(alternative_setting, Anime)

    def test_full_stories(self):
        self.assertIsInstance(self.tested_object.full_stories, frozenset)
        self.assertEqual(len(self.tested_object.full_stories), 0)
        for full_story in self.tested_object.full_stories:
            self.assertIsInstance(full_story, Anime)

    def test_str(self):
        self.tested_object.reload()
        self.assertEqual(str(self.tested_object), "<Anime Lucky☆Star id=1887>")


class NoReloadTestCase(unittest.TestCase):
    def setUp(self):
        self.tested_object = Anime(ANIME_ID)
        self.__reload = self.tested_object.reload
        self.tested_object.reload = Mock(wraps=self.__reload)

    def tearDown(self):
        self.assertFalse(self.tested_object.reload.called)
        Anime._unregiter(self.tested_object)

    def test_id(self):
        self.assertEqual(self.tested_object.id, ANIME_ID)

    def test_str(self):
        self.assertEqual(str(self.tested_object), '<Anime  id={0:d}>'.format(ANIME_ID))

    def test___equal___object(self):
        self.assertEqual(self.tested_object, self.tested_object)

    def test___equal___id_int(self):
        self.assertEqual(self.tested_object, ANIME_ID)

    def test___equal___id_str(self):
        self.assertEqual(self.tested_object, str(ANIME_ID))

    def test___equald___not_equal(self):
        self.assertNotEqual(self.tested_object, set())

    @unittest.skip("Delete is not working")
    def test_add_and_delete(self):
        account = Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        tested_object = Anime(ADD_ANIME_ID)
        my_tested_object = tested_object.add(account)

        self.assertIsInstance(my_tested_object, MyAnime)
        account.animes.reload()
        self.assertIn(my_tested_object, account.animes)

        my_tested_object.delete()
        account.animes.reload()
        self.assertNotIn(my_tested_object, account.animes)


def main():
    unittest.main()


if '__main__' == __name__:
    main()
