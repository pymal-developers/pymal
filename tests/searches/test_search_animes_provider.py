import unittest

from pymal.searches.search_animes_provider import SearchAnimesProvider
from pymal.anime import Anime

from tests.constants_for_testing import ANIME_ID


class SearchAnimesProviderTestCase(unittest.TestCase):
    def setUp(self):
        self.provider = SearchAnimesProvider()

    def tearDown(self):
        SearchAnimesProvider._instance = None

    def test_search(self):
        expected = frozenset({Anime(4472), Anime(ANIME_ID)})
        self.assertListEqual(self.provider.search('lucky star'), expected)
