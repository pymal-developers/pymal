__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

import hashlib

import bs4
from reloaded_set import load

from pymal import consts
from pymal.inner_objects.media import Media
from pymal import global_functions
from pymal import exceptions

__all__ = ['Anime']


class Anime(Media):
    """
    Object that keeps all the anime data in MAL.

    :ivar duration: :class:`int`
    :ivar rating: :class:`str`
    :ivar episodes: :class:`int`
    """

    _NAME = 'anime'
    _TIMING_HEADER = 'Aired'
    _CREATORS_HEADER = 'Producers'

    def __init__(self, mal_id: int):
        """
        :param mal_id: the anime id in mal.
        :type mal_id: int
        """
        super().__init__(mal_id)

        # Getting staff from html
        # staff from side content
        self.__duration = 0
        self.__rating = ''
        self.__episodes = 0

        self._side_bar_parser = [
            self._image_parse,
            self._void_parse,
            self._void_parse,
            self._void_parse,
            self._english_parse,
            self._synonyms_parse,
            self._japanese_parse,
            self._type_parse,
            self._episodes_parse,
            self._status_parse,
            self._timing_parse,
            self._creators_parse,
            self._genres_parse,
            self._duration_parse,
            self._rating_parse,
            self._score_parse,
            self._rank_parse,
            self._popularity_parse
        ]

    @property
    @load()
    def duration(self) -> int:
        return self.__duration

    @property
    @load()
    def rating(self) -> int:
        return self.__rating

    @property
    @load()
    def episodes(self) -> int:
        return self.__episodes

    def _episodes_parse(self, episodes_div: bs4.element.Tag):
        """
        :param episodes_div: Episodes <div>
        :type episodes_div: bs4.element.Tag
        :return: 1.
        """
        if not global_functions.check_side_content_div('Episodes', episodes_div):
            raise exceptions.FailedToReloadError(episodes_div)
        episodes_span, self_episodes = episodes_div.contents
        self.__episodes = global_functions.make_counter(self_episodes.strip())
        return 1

    def _duration_parse(self, duration_div: bs4.element.Tag):
        """
        :param duration_div: Duration <div>
        :type duration_div: bs4.element.Tag
        :return: 1.
        """
        if not global_functions.check_side_content_div('Duration', duration_div):
            raise exceptions.FailedToReloadError(duration_div)
        duration_span, duration_string = duration_div.contents
        self.__duration = 0
        duration_parts = duration_string.strip().split('.')
        duration_parts = list(map(lambda x: x.strip(), duration_parts))[:-1]
        for duration_part in duration_parts:
            number, scale = duration_part.split()
            number = int(number)
            if scale == 'min':
                self.__duration += number
            elif scale == 'hr':
                self.__duration += number * 60
            else:
                raise exceptions.FailedToReloadError('scale {0:s} is unknown'.format(scale))
        return 1

    def _rating_parse(self, rating_div: bs4.element.Tag):
        """
        :type rating_div: bs4.element.Tag
        :param rating_div: Rating <div>
        :return: 1.
        """
        if not global_functions.check_side_content_div('Rating', rating_div):
            raise exceptions.FailedToReloadError(rating_div)
        rating_span, self.__rating = rating_div.contents
        self.__rating = self.__rating.strip()
        return 1

    MY_MAL_XML_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<entry>
    <episode>{0:d}</episode>
    <status>{1:d}</status>
    <score>{2:d}</score>
    <downloaded_episodes>{3:d}</downloaded_episodes>
    <storage_type>{4:d}</storage_type>
    <storage_value>{5:f}</storage_value>
    <times_rewatched>{6:d}</times_rewatched>
    <rewatch_value>{7:d}</rewatch_value>
    <date_start>{8:s}</date_start>
    <date_finish>{9:s}</date_finish>
    <priority>{10:d}</priority>
    <enable_discussion>{11:d}</enable_discussion>
    <enable_rewatching>{12:d}</enable_rewatching>
    <comments>{13:s}</comments>
    <fansub_group>{14:s}</fansub_group>
    <tags>{15:s}</tags>
</entry>"""

    DEFAULT_ADDING = (0, 6, 0, 0, 0, 0, 0, 0, consts.MALAPI_NONE_TIME, consts.MALAPI_NONE_TIME, 0, False, False, '', '',
                      '', )

    def _add_data_checker(self, ret: str):
        """
        :param ret: The return value from mal api.
        :type ret: str
        :return: The added MyMedia id.
        :rtype: int
        :exception MyAnimeListApiAddError: if Failed to add.
        """
        html_obj = bs4.BeautifulSoup(ret)
        if html_obj is None:
            raise exceptions.MyAnimeListApiAddError(html_obj)

        head_obj = html_obj.head
        if head_obj is None:
            raise exceptions.MyAnimeListApiAddError(head_obj)

        title_obj = head_obj.title
        if title_obj is None:
            raise exceptions.MyAnimeListApiAddError(title_obj)

        data = title_obj.text
        if data is None:
            raise exceptions.MyAnimeListApiAddError(data)

        my_id, string = data.split()
        if not my_id.isdigit():
            raise exceptions.MyAnimeListApiAddError(my_id)
        if string != 'Created':
            raise exceptions.MyAnimeListApiAddError(string)
        return int(my_id)

    @property
    def _my_media(self):
        from pymal.account_objects.my_anime import MyAnime as MyMedia
        return MyMedia

    def __eq__(self, other):
        if isinstance(other, Anime):
            return self.id == other.id
        elif isinstance(other, int):
            return self.id == other
        elif isinstance(other, str) and other.isdigit():
            return self.id == int(other)
        elif hasattr(other, 'id'):
            return self.id == other.id
        return False

    def __hash__(self):
        hash_md5 = hashlib.md5()
        hash_md5.update(str(self.id).encode())
        hash_md5.update(self.__class__.__name__.encode())
        return int(hash_md5.hexdigest(), 16)