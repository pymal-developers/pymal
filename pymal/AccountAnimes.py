__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

import hashlib
from urllib import request, parse

import bs4

from pymal import consts
from pymal import decorators
from pymal import MyAnime

__all__ = ['AccountAnimes']


class AccountAnimes(object, metaclass=decorators.SingletonFactory):
    """
    """
    __all__ = ['watching', 'completed', 'on_hold', 'dropped', 'plan_to_watch',
               'reload']

    __URL = request.urljoin(consts.HOST_NAME, "animelist/{0:s}&status=")

    def __init__(self, username: str, connection):
        """
        """
        self.__connection = connection
        self.__url = self.__URL.format(username)

        self.__watching = set()
        self.__completed = set()
        self.__on_hold = set()
        self.__dropped = set()
        self.__plan_to_watch = set()

        self.map_of_lists = {
            1: self.__watching,
            2: self.__completed,
            3: self.__on_hold,
            4: self.__dropped,
            6: self.__plan_to_watch,

            '1': self.__watching,
            '2': self.__completed,
            '3': self.__on_hold,
            '4': self.__dropped,
            '6': self.__plan_to_watch,

            'watching': self.__watching,
            'completed': self.__completed,
            'onhold': self.__on_hold,
            'dropped': self.__dropped,
            'plantowatch': self.__plan_to_watch,
        }

        self._is_loaded = False

    @property
    @decorators.load
    def watching(self) -> set:
        return self.__watching

    @property
    @decorators.load
    def completed(self) -> set:
        return self.__completed

    @property
    @decorators.load
    def on_hold(self) -> set:
        return self.__on_hold

    @property
    @decorators.load
    def dropped(self) -> set:
        return self.__dropped

    @property
    @decorators.load
    def plan_to_watch(self) -> set:
        return self.__plan_to_watch

    def __contains__(self, item: MyAnime.MyAnime) -> bool:
        return any(map(lambda x: x == item, self))

    def __iter__(self):
        return iter(self.watching | self.completed | self.on_hold |
                    self.dropped | self.plan_to_watch)

    def reload(self):
        self.__watching = self.__get_my_animes(1)
        self.__completed = self.__get_my_animes(2)
        self.__on_hold = self.__get_my_animes(3)
        self.__dropped = self.__get_my_animes(4)
        self.__plan_to_watch = self.__get_my_animes(6)

        self._is_loaded = True

    def __get_my_animes(self, status: int) -> set:
        data = self.__connection.connect(self.__url + str(status))
        body = bs4.BeautifulSoup(data).body

        main_div = body.find(name='div', attrs={'id': 'list_surround'})
        tables = main_div.findAll(name='table', reucrsive=False)
        if 4 >= len(tables):
            return set()
        main_table = tables[3]
        rows = main_table.tbody.findAll(name='tr', recursive=False)

        return set(map(self.__parse_manga_div, rows))

    def __parse_manga_div(self, div: bs4.element.Tag) -> MyAnime.MyAnime:
        links_div = div.findAll(name='td', recorsive=False)[1]

        link = links_div.find(name='a', attrs={'class': 'animetitle'})
        link_id = int(link['href'].split('/')[2])

        if self.__connection.is_auth:
            my_link = links_div.find(name='a', attrs={'class': 'List_LightBox'})
            _, query = parse.splitquery(my_link['href'])
            my_link_id = int(parse.parse_qs(query)['id'][0])
        else:
            my_link_id = 0

        return MyAnime.MyAnime(link_id, my_link_id, self.__connection)

    def __len__(self):
        return len(frozenset(self))

    def __repr__(self):
        return "<User animes' number is {0:d}>".format(len(self))

    def __hash__(self):
        hash_md5 = hashlib.md5()
        hash_md5.update(self.__connection.username.encode())
        hash_md5.update(self.__class__.__name__.encode())
        return int(hash_md5.hexdigest(), 16)
