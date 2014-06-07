__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

from pymal import Account
from pymal.searches import Search

__all__ = ['SearchAccounts']


class SearchAccounts(Search.Search):
    _SEARCH_NAME = 'users'
    _SEARCHED_URL_SUFFIX = '/profile/'

    def _SEARCHED_OBJECT(self, mal_url: str) -> Account.Account:
        return Account.Account(mal_url)