__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

from urllib import parse

import bs4

from pymal import global_functions, consts, decorators

__all__ = ['SearchUsers', 'SearchAnimes', 'SearchMangas']


class Search(object, metaclass=decorators.Singleton):
    _SEARCH_NAME = ''
    _SEARCHED_URL_SUFFIX = ''
    _SEARCHED_OBJECT = object

    @property
    def __SEARCH_URL(self):
        return parse.urljoin(consts.HOST_NAME, self._SEARCH_NAME + '.php')

    def __make_url(self, search_line: str) -> str:
        params = {'q': search_line}
        url_parts = list(parse.urlparse(self.__SEARCH_URL))
        query = dict(parse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = parse.urlencode(query)
        return parse.urlunparse(url_parts)

    def __get_list(self, search_line: str) -> map:
        search_url = self.__make_url(search_line)

        sock = global_functions._connect(search_url)

        if sock.url != search_url:
            return map(lambda x: x, [parse.urlsplit(sock.url).path])

        html = bs4.BeautifulSoup(sock.text)
        div_content = html.find(name='div', attrs={'id': 'content'})
        divs_pic = div_content.findAll(name='div', attrs={'class': 'picSurround'})
        return map(lambda x: x.a['href'], divs_pic)

    def search(self, search_line: str) -> map:
        ret = list(self.__get_list(search_line))
        names = map(lambda x: x.split(self._SEARCHED_URL_SUFFIX)[1], ret)
        objects = map(lambda x: self._SEARCHED_OBJECT(x), names)
        return objects


class SearchUsers(Search):
    _SEARCH_NAME = 'users'
    _SEARCHED_URL_SUFFIX = '/profile/'
    from pymal import Account
    _SEARCHED_OBJECT = Account.Account


class SearchAnimes(Search):
    _SEARCH_NAME = 'anime'
    _SEARCHED_URL_SUFFIX = '/anime/'

    def _SEARCHED_OBJECT(self, mal_url: str):
        from pymal import Anime
        mal_id = int(mal_url.split('/')[0])
        return Anime.Anime(int(mal_id))


class SearchMangas(Search):
    _SEARCH_NAME = 'manga'
    _SEARCHED_URL_SUFFIX = '/manga/'

    def _SEARCHED_OBJECT(self, mal_url: str):
        from pymal import Manga
        mal_id = int(mal_url.split('/')[0])
        return Manga.Manga(int(mal_id))
