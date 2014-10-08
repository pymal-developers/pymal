import unittest

from pymal.searches.search_accounts_provider import SearchAccountsProvider
from pymal.account import Account

from tests.constants_for_testing import ACCOUNT_TEST_USERNAME


class SearchAccountsProviderTestCase(unittest.TestCase):
    def setUp(self):
        self.provider = SearchAccountsProvider()

    def tearDown(self):
        SearchAccountsProvider._instance = None

    def test_search(self):
        expected = frozenset({Account(ACCOUNT_TEST_USERNAME)})
        self.assertSequenceEqual(self.provider.search(ACCOUNT_TEST_USERNAME), expected)
