__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

from pymal.searches import SearchAccounts, SearchAnimes, SearchMangas

__all__ = ['search_animes', 'search_mangas', 'search_accounts']

__SearchAccounts = SearchAccounts.SearchAccounts()
__SearchAnimes = SearchAnimes.SearchAnimes()
__SearchMangas = SearchMangas.SearchMangas()


def search_accounts(search_string: str) -> map:
    return __SearchAccounts.search(search_string)


def search_animes(search_string: str) -> map:
    return __SearchAnimes.search(search_string)


def search_mangas(search_string: str) -> map:
    return __SearchMangas.search(search_string)
