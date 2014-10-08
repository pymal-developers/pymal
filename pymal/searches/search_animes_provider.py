__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

from pymal.searches import search_provider

__all__ = ['SearchAnimesProvider']


class SearchAnimesProvider(search_provider.SearchProvider):
    """
    Searching for animes.
    """
    @property
    def _SEARCH_NAME(self):
        return 'anime'

    @property
    def _SEARCHED_URL_SUFFIX(self):
        return '/anime/'

    def _SEARCHED_OBJECT(self, mal_url: str):
        from pymal.anime import Anime

        mal_id = int(mal_url.split('/')[0])
        return Anime(int(mal_id))
