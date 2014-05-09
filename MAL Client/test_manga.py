import unittest
from Manga import Manga
from constants_for_testing import MANGA_ID


class MangaTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manga = Manga(MANGA_ID)

    def test_manga_title(self):
        self.assertEqual(self.manga.title, 'Lucky☆Star')

    def test_manga_spinoff(self):
        self.assertGreater(len(self.manga.spin_offs), 0 )
        for spin_off in self.manga.spin_offs:
            self.assertEqual(spin_off.__class__, Manga)


def main():
    unittest.main()


if '__main__' == __name__:
    main()