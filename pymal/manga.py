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

__all__ = ['Manga']


class Manga(Media):
    """
    Object that keeps all the anime data in MAL.

    :ivar chapters: :class:`int`
    :ivar volumes: :class:`int`
    """

    _NAME = 'manga'
    _TIMING_HEADER = 'Published'
    _CREATORS_HEADER = 'Authors'

    def __init__(self, mal_id: int):
        """
        :param mal_id: the manga id in mal.
        :type mal_id: int
        """
        super().__init__(mal_id)

        # Getting staff from html
        # staff from side content
        self._chapters = 0
        self._volumes = 0

        self._side_bar_parser = [
            self._image_parse,
            self._void_parse,
            self._void_parse,
            self._english_parse,
            self._synonyms_parse,
            self._japanese_parse,
            self._type_parse,
            self._volumes_parse,
            self._chapters_parse,
            self._status_parse,
            self._timing_parse,
            self._genres_parse,
            self._creators_parse,
            self._void_parse,
            self._score_parse,
            self._rank_parse,
            self._popularity_parse
        ]

    @property
    @load()
    def volumes(self) -> int:
        return self.__volumes

    @property
    @load()
    def chapters(self) -> int:
        return self.__chapters

    def _volumes_parse(self, volumes_div: bs4.element.Tag):
        """
        :param volumes_div: Volumes <div>
        :type volumes_div: bs4.element.Tag
        :return: 1.
        """
        if not global_functions.check_side_content_div('Volumes', volumes_div):
            raise exceptions.FailedToReloadError(volumes_div)
        volumes_span, self_volumes = volumes_div.contents
        self.__volumes = global_functions.make_counter(self_volumes.strip())
        return 1

    def _chapters_parse(self, chapters_div: bs4.element.Tag):
        """
        :param chapters_div: Chapters <div>
        :type chapters_div: bs4.element.Tag
        :return: 1.
        """
        if not global_functions.check_side_content_div('Chapters', chapters_div):
            raise exceptions.FailedToReloadError(chapters_div)
        chapters_span, self_chapters = chapters_div.contents
        self.__chapters = global_functions.make_counter(self_chapters.strip())
        return 1


    MY_MAL_XML_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<entry>
	<chapter>{0:d}</chapter>
	<volume>{1:d}</volume>
	<status>{2:d}</status>
	<score>{3:d}</score>
	<downloaded_chapters>{4:d}</downloaded_chapters>
	<times_reread>{5:d}</times_reread>
	<reread_value>{6:d}</reread_value>
	<date_start>{7:s}</date_start>
	<date_finish>{8:s}</date_finish>
	<priority>{9:d}</priority>
	<enable_discussion>{10:d}</enable_discussion>
	<enable_rereading>{11:d}</enable_rereading>
	<comments>{12:s}</comments>
	<scan_group>{13:s}</scan_group>
	<tags>{14:s}</tags>
	<retail_volumes>{15:d}</retail_volumes>
</entry>"""

    DEFAULT_ADDING = (0, 0, 6, 0, 0, 0, 0, consts.MALAPI_NONE_TIME, consts.MALAPI_NONE_TIME, 0, False, False, '', '',
                      '', 0, )

    def _add_data_checker(self, ret: str):
        """
        :param ret: The return value from mal api.
        :type ret: str
        :return: The added MyMedia id.
        :rtype: int
        :exception MyAnimeListApiAddError: if Failed to add.
        """
        if not ret.isdigit():
            raise exceptions.MyAnimeListApiAddError(ret)
        return int(ret)

    @property
    def _my_media(self):
        from pymal.account_objects.my_anime import MyAnime as MyMedia
        return MyMedia

    def __eq__(self, other):
        if isinstance(other, Manga):
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