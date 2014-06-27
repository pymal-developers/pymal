import unittest

from pymal import Account
from pymal import Anime
from pymal import Manga
from pymal.account_objects import MyManga

from tests.constants_for_testing import MANGA_ID, ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD


class ReloadTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.manga = Manga.Manga(MANGA_ID)
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
            self.assertIsInstance(spin_off, Manga.Manga)

    def test_manga_adaptations(self):
        self.assertIsInstance(self.manga.adaptations, frozenset)
        for adaptation in self.manga.adaptations:
            self.assertIsInstance(adaptation, Anime.Anime)

    def test_manga_characters(self):
        self.assertIsInstance(self.manga.characters, frozenset)
        for character in self.manga.characters:
            self.assertIsInstance(character, Manga.Manga)

    def test_manga_sequals(self):
        self.assertIsInstance(self.manga.sequels, frozenset)
        for sequal in self.manga.sequels:
            self.assertIsInstance(sequal, Manga.Manga)

    def test_manga_prequel(self):
        self.assertIsInstance(self.manga.prequels, frozenset)
        for prequel in self.manga.prequels:
            self.assertIsInstance(prequel, Manga.Manga)

    def test_manga_alternative_versions(self):
        self.assertIsInstance(self.manga.alternative_versions, frozenset)
        for alternative_version in self.manga.alternative_versions:
            self.assertIsInstance(alternative_version, Manga.Manga)

    def test_manga_side_story(self):
        self.assertIsInstance(self.manga.side_stories, frozenset)
        for side_story in self.manga.side_stories:
            self.assertIsInstance(side_story, Manga.Manga)

    def test_manga_summaries(self):
        self.assertIsInstance(self.manga.summaries, frozenset)
        for summary in self.manga.summaries:
            self.assertIsInstance(summary, Manga.Manga)

    def test_manga_other(self):
        self.assertIsInstance(self.manga.others, frozenset)
        for other in self.manga.others:
            self.assertIsInstance(other, Manga.Manga)

    def test_manga_parent_stories(self):
        self.assertIsInstance(self.manga.parent_stories, frozenset)
        for parent_story in self.manga.parent_stories:
            self.assertIsInstance(parent_story, Manga.Manga)

    def test_manga_alternative_settings(self):
        self.assertIsInstance(self.manga.alternative_settings, frozenset)
        for alternative_setting in self.manga.alternative_settings:
            self.assertIsInstance(alternative_setting, Manga.Manga)

    def test_str(self):
        repr(self.manga)


class NoReloadTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.account = Account.Account(ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD)
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

    def test_add_and_delete(self):
        manga = Manga.Manga(11)
        my_manga = manga.add(self.account)
        try:
            self.assertIsInstance(my_manga, MyManga.MyManga)
            self.account.mangas.reload()
            self.assertIn(my_manga, self.account.mangas)
        finally:
            my_manga.delete()

        self.account.mangas.reload()
        self.assertNotIn(my_manga, self.account.mangas)


def main():
    unittest.main()


if '__main__' == __name__:
    main()