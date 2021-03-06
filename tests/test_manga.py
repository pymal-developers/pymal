import unittest

from pymal import account
from pymal import anime
from pymal import manga
from pymal.account_objects import my_manga

from tests.constants_for_testing import ADD_MANGA_ID, MANGA_ID, ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD


class ReloadTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.manga = manga.Manga(MANGA_ID)
        cls.manga.reload()

    def test_manga_id(self):
        self.assertEqual(self.manga.id, MANGA_ID)

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
        repr(self.manga)


class NoReloadTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.account = account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
        cls.manga = list(cls.account.mangas)[0]

    def test_id(self):
        self.assertIsInstance(self.manga.id, int)

    def test_title(self):
        self.assertIsInstance(self.manga.english, str)

    def test_image_url(self):
        self.assertIsInstance(self.manga.image_url, str)

    def test_synonyms(self):
        self.assertIsInstance(self.manga.synonyms, str)

    def test_type(self):
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

    def test_start_time(self):
        self.assertIsInstance(self.manga.start_time, float)

    def test_end_time(self):
        self.assertIsInstance(self.manga.end_time, float)

    def test_str(self):
        repr(self.manga)

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
