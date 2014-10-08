import unittest
from mock import Mock
from os import path

import bs4
from pymal.account import Account
from pymal.anime import Anime
from pymal.manga import Manga
from pymal import global_functions
from pymal.account_objects.my_manga import MyManga

from tests.constants_for_testing import ADD_MANGA_ID, MANGA_ID, ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD,\
    SOURCES_DIRECTORY


class FetchWebTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tested_object = Manga(MANGA_ID)

    def test_fetch_web(self):
        self.tested_object.reload()


class ReloadTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.__global_functions_get_content_wrapper_div = global_functions.get_content_wrapper_div

        with open(path.join(SOURCES_DIRECTORY, 'Lucky☆Star manga - MyAnimeList.net.html'), "rb") as f:
            data = f.read().decode()
        html = bs4.BeautifulSoup(data, "html5lib")
        myanimelist_div = html.body.find(name="div", attrs={"id": 'myanimelist'})
        content_wrapper_div = myanimelist_div.find(name="div", attrs={"id": "contentWrapper"}, recursive=False)
        global_functions.get_content_wrapper_div = Mock(return_value=content_wrapper_div)

    def setUp(self):
        self.tested_object = Manga(MANGA_ID)
        self.__reload = self.tested_object.reload
        self.tested_object.reload = Mock(wraps=self.__reload)

    @classmethod
    def tearDownClass(cls):
        global_functions.get_content_wrapper_div = cls.__global_functions_get_content_wrapper_div

    def tearDown(self):
        self.tested_object.reload.assert_called_once_with()
        Manga._unregiter(self.tested_object)

    def test_title(self):
        self.assertEqual(self.tested_object.title, 'Lucky☆Star')

    def test_image_url(self):
        self.assertIsInstance(self.tested_object.image_url, str)

    def test_english(self):
        self.assertEqual(self.tested_object.english, 'Lucky ☆ Star')

    def test_synonyms(self):
        self.assertIsInstance(self.tested_object.synonyms, str)

    def test_japanese(self):
        self.assertIsInstance(self.tested_object.japanese, str)

    def test_type(self):
        self.assertIsInstance(self.tested_object.type, str)

    def test_status(self):
        self.assertIsInstance(self.tested_object.status, str)

    def test_chapters(self):
        try:
            self.assertIsInstance(self.tested_object.chapters, int)
        except AssertionError:
            self.assertEqual(self.tested_object.chapters, float('inf'))
            self.assertEqual(self.tested_object.chapters, self.tested_object.volumes)

    def test_volumes(self):
        try:
            self.assertIsInstance(self.tested_object.volumes, int)
        except AssertionError:
            self.assertEqual(self.tested_object.volumes, float('inf'))

    def test_start_time(self):
        self.assertIsInstance(self.tested_object.start_time, float)

    def test_end_time(self):
        self.assertIsInstance(self.tested_object.end_time, float)

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
        self.assertIsInstance(self.tested_object.synopsis, str)

    def test_spinoff(self):
        self.assertIsInstance(self.tested_object.spin_offs, frozenset)
        for spin_off in self.tested_object.spin_offs:
            self.assertIsInstance(spin_off, Manga)

    def test_adaptations(self):
        self.assertIsInstance(self.tested_object.adaptations, frozenset)
        for adaptation in self.tested_object.adaptations:
            self.assertIsInstance(adaptation, Anime)

    def test_characters(self):
        self.assertIsInstance(self.tested_object.characters, frozenset)
        for character in self.tested_object.characters:
            self.assertIsInstance(character, Manga)

    def test_sequals(self):
        self.assertIsInstance(self.tested_object.sequels, frozenset)
        for sequal in self.tested_object.sequels:
            self.assertIsInstance(sequal, Manga)

    def test_prequels(self):
        self.assertIsInstance(self.tested_object.prequels, frozenset)
        for prequel in self.tested_object.prequels:
            self.assertIsInstance(prequel, Manga)

    def test_alternative_versions(self):
        self.assertIsInstance(self.tested_object.alternative_versions, frozenset)
        for alternative_version in self.tested_object.alternative_versions:
            self.assertIsInstance(alternative_version, Manga)

    def test_side_story(self):
        self.assertIsInstance(self.tested_object.side_stories, frozenset)
        for side_story in self.tested_object.side_stories:
            self.assertIsInstance(side_story, Manga)

    def test_summaries(self):
        self.assertIsInstance(self.tested_object.summaries, frozenset)
        for summary in self.tested_object.summaries:
            self.assertIsInstance(summary, Manga)

    def test_other(self):
        self.assertIsInstance(self.tested_object.others, frozenset)
        for other in self.tested_object.others:
            self.assertIsInstance(other, Manga)

    def test_parent_stories(self):
        self.assertIsInstance(self.tested_object.parent_stories, frozenset)
        for parent_story in self.tested_object.parent_stories:
            self.assertIsInstance(parent_story, Manga)

    def test_alternative_settings(self):
        self.assertIsInstance(self.tested_object.alternative_settings, frozenset)
        for alternative_setting in self.tested_object.alternative_settings:
            self.assertIsInstance(alternative_setting, Manga)

    def test_full_stories(self):
        self.assertIsInstance(self.tested_object.full_stories, frozenset)
        self.assertEqual(len(self.tested_object.full_stories), 0)
        for full_story in self.tested_object.full_stories:
            self.assertIsInstance(full_story, Manga)

    def test_str(self):
        self.tested_object.reload()
        self.assertEqual(str(self.tested_object), '<Manga Lucky☆Star id=587>')


class NoReloadTestCase(unittest.TestCase):
    def setUp(self):
        self.tested_object = Manga(MANGA_ID)
        self.__reload = self.tested_object.reload
        self.tested_object.reload = Mock(wraps=self.__reload)

    def tearDown(self):
        self.assertFalse(self.tested_object.reload.called)
        Manga._unregiter(self.tested_object)

    def test_id(self):
        self.assertIsInstance(self.tested_object.id, int)

    def test_str(self):
        self.assertEqual(str(self.tested_object), '<Manga  id=587>')

    def test___equal___object(self):
        self.assertEqual(self.tested_object, self.tested_object)

    def test___equal___id_int(self):
        self.assertEqual(self.tested_object, MANGA_ID)

    def test___equal___id_str(self):
        self.assertEqual(self.tested_object, str(MANGA_ID))

    def test___equald___not_equal(self):
        self.assertNotEqual(self.tested_object, set())

    @unittest.skip("Delete is not working")
    def test_add_and_delete(self):
        account = Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        tested_object = Manga(ADD_MANGA_ID)
        my_tested_object = tested_object.add(account)

        self.assertIsInstance(my_tested_object, MyManga)
        account.mangas.reload()
        self.assertIn(my_tested_object, account.mangas)

        my_tested_object.delete()
        account.mangas.reload()
        self.assertNotIn(my_tested_object, account.mangas)


def main():
    unittest.main()


if '__main__' == __name__:
    main()
