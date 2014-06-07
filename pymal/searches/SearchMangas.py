__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

from pymal import Manga
from pymal.searches import Search

__all__ = ['SearchMangas']


class SearchMangas(Search.Search):
    _SEARCH_NAME = 'manga'
    _SEARCHED_URL_SUFFIX = '/manga/'

    def _SEARCHED_OBJECT(self, mal_url: str) -> Manga.Manga:
        mal_id = int(mal_url.split('/')[0])
        return Manga.Manga(int(mal_id))
