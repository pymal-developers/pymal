__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

import os

import requests
import bs4

from pymal import decorators
from pymal import Season

__all__ = ['Seasons']


class Seasons(object, metaclass=decorators.Singleton):
    """
    Lazy making of Season from online db.
    
    Attributes:
        seasons: set of Season.
    """
    __all__ = ['seasons', 'reload']

    __SEASONS_URL = 'http://malupdater.com/MalUpdater/Seasons/index.txt'

    def __init__(self):
        self.__seasons = set()
        self._is_loaded = False

    @property
    @decorators.load
    def seasons(self) -> frozenset:
        return self.__seasons

    def reload(self):
        sock = requests.get(self.__SEASONS_URL)
        seasons_lines = bs4.BeautifulSoup(sock.text).body.text.splitlines()

        seasons = set()
        for season_line in seasons_lines:
            year, seasons_name = season_line.split('_')
            seasons.add(Season.Season(seasons_name, year))
        self.__seasons = frozenset(seasons)

        self._is_loaded = True

    def __contains__(self, item) -> bool:
        return any(map(lambda x: item in x, self.seasons))

    def __repr__(self):
        return (os.linesep + '\t').join(map(str, ['<Seasons>'] +
                                            list(self.seasons)))

    def __iter__(self):
        return iter(self.seasons)

    def __len__(self) -> int:
        return sum(map(lambda x: len(x), self.seasons))
