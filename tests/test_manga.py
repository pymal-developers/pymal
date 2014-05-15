import unittest
from pymal.Manga import Manga
from tests.constants_for_testing import MANGA_ID


class MangaTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manga = Manga(MANGA_ID)

    def test_manga_id(self):
        self.assertIsInstance(self.manga.id, int)
        self.assertEqual(self.manga.id, MANGA_ID)

    def test_manga_title(self):
        self.assertIsInstance(self.manga.english, str)
        self.assertEqual(self.manga.english, 'Lucky☆Star')

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
        self.assertIsInstance(self.manga.chapters, int)

    def test_manga_volumes(self):
        self.assertIsInstance(self.manga.volumes, int)

    def test_manga_start_time(self):
        self.assertTrue(self.manga.start_time == float('inf') or type(self.manga.start_time) == int)

    def test_manga_end_time(self):
        self.assertTrue(self.manga.end_time == float('inf') or type(self.manga.end_time) == int)


    def test_manga_rating(self):
        self.assertIsInstance(self.manga.rating, int)

    def test_manga_score(self):
        self.assertIsInstance(self.manga.score, float)

    def test_manga_rank(self):
        self.assertIsInstance(self.manga.rank, int)

    def test_manga_popularity(self):
        self.assertIsInstance(self.manga.popularity, int)

    def test_manga_synopsis(self):
        self.assertIsInstance(self.manga.synopsis, str)

    def test_manga_spinoff(self):
        self.assertIsInstance(self.manga.spin_offs, set)
        for spin_off in self.manga.spin_offs:
            self.assertIsInstance(spin_off, Manga)

    def test_manga_adaptations(self):
        self.assertIsInstance(self.manga.adaptations, set)
        for adaptation in self.manga.adaptations:
            self.assertIsInstance(adaptation, Manga)

    def test_manga_characters(self):
        self.assertIsInstance(self.manga.characters, set)
        for character in self.manga.characters:
            self.assertIsInstance(character, str)

    def test_manga_sequals(self):
        self.assertIsInstance(self.manga.sequals, set)
        for sequal in self.manga.sequals:
            self.assertIsInstance(sequal, Manga)

    def test_manga_prequel(self):
        self.assertIsInstance(self.manga.prequel, set)
        for preque in self.manga.prequel:
            self.assertIsInstance(preque, Manga)

    def test_manga_spinoffs(self):
        self.assertIsInstance(self.manga.spin_offs, set)
        for spin_off in self.manga.spin_offs:
            self.assertIsInstance(spin_off, Manga)

    def test_manga_alternative_versions(self):
        self.assertIsInstance(self.manga.alternative_versions, set)
        for alternative_version in self.manga.alternative_versions:
            self.assertIsInstance(alternative_version, Manga)

    def test_manga_side_story(self):
        self.assertIsInstance(self.manga.side_stories, set)
        for side_story in self.manga.side_stories:
            self.assertIsInstance(side_story, Manga)

    def test_manga_summaries(self):
        self.assertIsInstance(self.manga.summaries, set)
        for summary in self.manga.summaries:
            self.assertIsInstance(summary, Manga)

    def test_manga_other(self):
        self.assertIsInstance(self.manga.others, set)
        for other in self.manga.others:
            self.assertIsInstance(other, Manga)

    def test_manga_parent_stories(self):
        self.assertIsInstance(self.manga.parent_stories, set)
        for parent_story in self.manga.parent_stories:
            self.assertIsInstance(parent_story, Manga)

    def test_manga_alternative_settings(self):
        self.assertIsInstance(self.manga.alternative_settings, set)
        for alternative_setting in self.manga.alternative_settings:
            self.assertIsInstance(alternative_setting, Manga)


def main():
    unittest.main()


if '__main__' == __name__:
    main()