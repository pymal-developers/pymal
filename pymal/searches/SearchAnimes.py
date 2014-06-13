__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

from pymal import Anime
from pymal.searches import Search

__all__ = ['SearchAnimes']


class SearchAnimes(Search.Search):
    _SEARCH_NAME = 'anime'
    _SEARCHED_URL_SUFFIX = '/anime/'

    def _SEARCHED_OBJECT(self, mal_url: str) -> Anime.Anime:
        mal_id = int(mal_url.split('/')[0])
        return Anime.Anime(int(mal_id))
