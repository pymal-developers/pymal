import unittest
from mock import Mock
from os import path

import bs4
from pymal import anime
from pymal import manga
from pymal.account_objects import my_manga
from pymal import global_functions

from tests.constants_for_testing import ADD_MANGA_ID, MANGA_ID, SOURCES_DIRECTORY


class FetchWebTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manga = manga.Manga(MANGA_ID)

    def test_fetch_web(self):
        self.manga.reload()


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

    @classmethod
    def tearDownClass(cls):
        global_functions.get_content_wrapper_div = cls.__global_functions_get_content_wrapper_div

    def setUp(self):
        self.manga = manga.Manga(MANGA_ID)
        self.__reload = self.manga.reload
        self.manga.reload = Mock(wraps=self.__reload)

    def tearDown(self):
        self.manga.reload.assert_called_once_with()
        manga.Manga._unregiter(self.manga)

    def test_manga_title(self):
        self.assertEqual(self.manga.english, 'Lucky ☆ Star')

    def test_manga_image_url(self):
        self.assertIsInstance(self.manga.image_url, str)

    def test_manga_english(self):
        self.assertIsInstance(self.manga.english, str)

    def test_manga_synonyms(self):
        self.assertIsInstance(self.manga.synonyms, str)

    def test_manga_japanese(self):
        self.assertIsInstance(self.manga.japanese, str)

    def test_manga_type(self):
        self.assertIsInstance(self.manga.type, str)

    def test_manga_chapters(self):
        try:
            self.assertIsInstance(self.manga.chapters, int)
        except AssertionError:
            self.assertEqual(self.manga.chapters, float('inf'))
            self.assertEqual(self.manga.chapters, self.manga.volumes)

    def test_manga_volumes(self):
        try:
            self.assertIsInstance(self.manga.volumes, int)
        except AssertionError:
            self.assertEqual(self.manga.volumes, float('inf'))

    def test_manga_start_time(self):
        self.assertIsInstance(self.manga.start_time, float)

    def test_manga_end_time(self):
        self.assertIsInstance(self.manga.end_time, float)

    def test_manga_score(self):
        self.assertIsInstance(self.manga.score, float)

    def test_manga_rank(self):
        self.assertIsInstance(self.manga.rank, int)

    def test_manga_popularity(self):
        self.assertIsInstance(self.manga.popularity, int)

    def test_manga_synopsis(self):
        self.assertIsInstance(self.manga.synopsis, str)

    def test_manga_spinoff(self):
        self.assertIsInstance(self.manga.spin_offs, frozenset)
        for spin_off in self.manga.spin_offs:
            self.assertIsInstance(spin_off, manga.Manga)

    def test_manga_adaptations(self):
        self.assertIsInstance(self.manga.adaptations, frozenset)
        for adaptation in self.manga.adaptations:
            self.assertIsInstance(adaptation, anime.Anime)

    def test_manga_characters(self):
        self.assertIsInstance(self.manga.characters, frozenset)
        for character in self.manga.characters:
            self.assertIsInstance(character, manga.Manga)

    def test_manga_sequals(self):
        self.assertIsInstance(self.manga.sequels, frozenset)
        for sequal in self.manga.sequels:
            self.assertIsInstance(sequal, manga.Manga)

    def test_manga_prequel(self):
        self.assertIsInstance(self.manga.prequels, frozenset)
        for prequel in self.manga.prequels:
            self.assertIsInstance(prequel, manga.Manga)

    def test_manga_alternative_versions(self):
        self.assertIsInstance(self.manga.alternative_versions, frozenset)
        for alternative_version in self.manga.alternative_versions:
            self.assertIsInstance(alternative_version, manga.Manga)

    def test_manga_side_story(self):
        self.assertIsInstance(self.manga.side_stories, frozenset)
        for side_story in self.manga.side_stories:
            self.assertIsInstance(side_story, manga.Manga)

    def test_manga_summaries(self):
        self.assertIsInstance(self.manga.summaries, frozenset)
        for summary in self.manga.summaries:
            self.assertIsInstance(summary, manga.Manga)

    def test_manga_other(self):
        self.assertIsInstance(self.manga.others, frozenset)
        for other in self.manga.others:
            self.assertIsInstance(other, manga.Manga)

    def test_manga_parent_stories(self):
        self.assertIsInstance(self.manga.parent_stories, frozenset)
        for parent_story in self.manga.parent_stories:
            self.assertIsInstance(parent_story, manga.Manga)

    def test_manga_alternative_settings(self):
        self.assertIsInstance(self.manga.alternative_settings, frozenset)
        for alternative_setting in self.manga.alternative_settings:
            self.assertIsInstance(alternative_setting, manga.Manga)

    def test_str(self):
        self.manga.reload()
        self.assertEqual(str(self.manga), '<Manga Lucky☆Star id=587>')


class NoReloadTestCase(unittest.TestCase):

    def setUp(self):
        self.manga = manga.Manga(MANGA_ID)
        self.__reload = self.manga.reload
        self.manga.reload = Mock(wraps=self.__reload)

    def tearDown(self):
        self.assertFalse(self.manga.reload.called)
        manga.Manga._unregiter(self.manga)

    def test_id(self):
        self.assertIsInstance(self.manga.id, int)

    def test_str(self):
        self.assertEqual(str(self.manga), '<Manga  id=587>')

    def test___equal___manga_object(self):
        self.assertEqual(self.manga, self.manga)

    def test___equal___manga_id_int(self):
        self.assertEqual(self.manga, MANGA_ID)

    def test___equal___manga_id_str(self):
        self.assertEqual(self.manga, str(MANGA_ID))

    def test___equald___not_equal(self):
        self.assertNotEqual(self.manga, set())

    @unittest.skip("Delete is not working")
    def test_add_and_delete(self):
        mng = manga.Manga(ADD_MANGA_ID)
        my_mng = mng.add(self.account)

        self.assertIsInstance(my_mng, my_manga.MyManga)
        self.account.mangas.reload()
        self.assertIn(my_mng, self.account.mangas)

        my_mng.delete()
        self.account.mangas.reload()
        self.assertNotIn(my_mng, self.account.mangas)


def main():
    unittest.main()


if '__main__' == __name__:
    main()
