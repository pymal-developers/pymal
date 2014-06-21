__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

import hashlib
import time

import requests
import bs4

from pymal import decorators
from pymal.types import SingletonFactory
from pymal import exceptions
from pymal import Anime

__all__ = ['Season']


class Season(object, metaclass=SingletonFactory):
    """
    Lazy load of season data.
    
    Attributes:
        animes - a frozenset of animes.
        year - the season year.
        season_name - The season name.
          Can be 'Winter', 'Spring', 'Summer' or 'Fall'.
    """
    __all__ = ['animes', 'reload']

    __SEASON_URL = "http://malupdater.com/MalUpdater/Seasons/{0:d}_{1:s}.xml"
    __SEAONS_NAME_TO_START_MONTH = {
        'Winter': 1,
        'Spring': 4,
        'Summer': 7,
        'Fall': 10
    }

    def __init__(self, season_name: str, year: int or str):
        """
        """
        self.year = int(year)
        self.season_name = season_name.title()
        if self.season_name not in self.__SEAONS_NAME_TO_START_MONTH:
            raise exceptions.NotASeason(season_name)
        self.url = self.__SEASON_URL.format(self.year, self.season_name)

        self._is_loaded = False
        self.__animes = frozenset()

        month = str(self.__SEAONS_NAME_TO_START_MONTH[self.season_name])
        start_time_string = str(year) + ' ' + month
        self.start_time = time.strptime(start_time_string, '%Y %m')

    @property
    @decorators.load
    def animes(self) -> frozenset:
        return self.__animes

    def reload(self):
        sock = requests.get(self.url)
        xml = bs4.BeautifulSoup(sock.text)
        animes_xml = frozenset(xml.body.findAll(name='anime', recursive=False))
        animes_xml_with_id = frozenset(filter(lambda x: x.malid.text.isdigit(), animes_xml))
        if 0 != len(animes_xml - animes_xml_with_id):
            print("animes with no id:",animes_xml - animes_xml_with_id)
        animes_ids = map(lambda x: int(x.malid.text), animes_xml_with_id)
        self.__animes = frozenset(map(lambda x: Anime.Anime(x), animes_ids))

    def __iter__(self):
        return iter(self.animes)

    def __len__(self):
        return len(self.animes)

    def __hash__(self):
        hash_md5 = hashlib.md5()
        hash_md5.update(str(self.year).encode())
        hash_md5.update(self.season_name.encode())
        return int(hash_md5.hexdigest(), 16)

    def __repr__(self):
        return "<{0:s} {1:s} {2:d}>".format(self.__class__.__name__,
                                            self.season_name, self.year)
