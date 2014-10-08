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

    :ivar title: :class:`str`
    :ivar image_url: :class:`str`
    :ivar english: :class:`str`
    :ivar synonyms: :class:`str`
    :ivar japanese: :class:`str`
    :ivar type: :class:`str`
    :ivar status: :class:`int`
    :ivar start_time: :class:`int`
    :ivar end_time: :class:`int`
    :ivar creators: :class:`dict`
    :ivar genres: :class:`dict`
    :ivar duration: :class:`int`
    :ivar score: :class:`float`
    :ivar rank: :class:`int`
    :ivar popularity: :class:`int`
    :ivar rating: :class:`str`
    :ivar chapters: :class:`int`
    :ivar volumes: :class:`int`
    :ivar synopsis: :class:`str`

    :ivar adaptations: :class:`frozenset`
    :ivar characters: :class:`frozenset`
    :ivar sequels: :class:`frozenset`
    :ivar prequels: :class:`frozenset`
    :ivar spin_offs: :class:`frozenset`
    :ivar alternative_versions: :class:`frozenset`
    :ivar side_stories: :class:`frozenset`
    :ivar summaries: :class:`frozenset`
    :ivar others: :class:`frozenset`
    :ivar parent_stories: :class:`frozenset`
    :ivar alternative_settings: :class:`frozenset`
    """

    _NAME = 'manga'

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
            self._published_parse,
            self._genres_parse,
            self._authors_parse,
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

    def _published_parse(self, published_div: bs4.element.Tag):
        """
        :param published_div: Published <div>
        :type published_div: bs4.element.Tag
        :return: 1.
        """
        if not global_functions.check_side_content_div('Published', published_div):
            raise exceptions.FailedToReloadError(published_div)
        published_span, published = published_div.contents
        self._start_time, self._end_time = global_functions.make_start_and_end_time(published)
        return 1

    def _authors_parse(self, authors_div: bs4.element.Tag):
        """
        :param authors_div: Authors <div>
        :type authors_div: bs4.element.Tag
        :return: 1.
        """
        if not global_functions.check_side_content_div('Authors', authors_div):
            raise exceptions.FailedToReloadError(authors_div)
        for authors_link in authors_div.findAll(name='a'):
            self._creators[authors_link.text.strip()] = authors_link['href']
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