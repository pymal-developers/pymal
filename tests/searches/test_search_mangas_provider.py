import unittest

from pymal.searches.search_mangas_provider import SearchMangasProvider
from pymal.manga import Manga


class SearchMangasProviderTestCase(unittest.TestCase):
    def setUp(self):
        self.provider = SearchMangasProvider()

    def tearDown(self):
        SearchMangasProvider._instance = None

    def test_search(self):
        expected = frozenset({Manga(19017), Manga(587), Manga(13645), Manga(12379), Manga(60025), Manga(4505)})
        self.assertSequenceEqual(self.provider.search('lucky star'), expected)
