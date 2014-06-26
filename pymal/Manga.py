__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

import hashlib
from urllib import request
import os
import io

from PIL import Image
import requests
import bs4

from pymal import decorators
from pymal.types import SingletonFactory
from pymal import consts
from pymal import global_functions
from pymal import exceptions

__all__ = ['Manga']


class Manga(object, metaclass=SingletonFactory.SingletonFactory):
    """
    """
    __all__ = ['id', 'title', 'image_url', 'english', 'synonyms', 'japanese',
               'type', 'status', 'start_time', 'end_time', 'creators',
               'genres', 'score', 'rank', 'popularity', 'synopsis',
               'adaptations', 'characters', 'sequels', 'prequel', 'spin_offs',
               'alternative_versions', 'side_stories', 'summaries', 'others',
               'parent_stories', 'alternative_settings', 'volumes', 'chapters',
               'reload', 'add']
    
    __GLOBAL_MAL_URL = request.urljoin(consts.HOST_NAME, "manga/{0:d}")
    __MY_MAL_ADD_URL = request.urljoin(
        consts.HOST_NAME, 'api/mangalist/add/{0:d}.xml')

    def __init__(self, mal_id: int):
        """
        """
        self.__id = mal_id
        self._is_loaded = False

        self.__mal_url = self.__GLOBAL_MAL_URL.format(self.__id)

        # Getting staff from html
        # staff from side content
        self.__title = ''
        self.__image_url = ''
        self.__english = ''
        self.__synonyms = ''
        self.__japanese = ''
        self.__type = ''
        self.__status = 0
        self.__start_time = 0
        self.__end_time = 0
        self.__creators = dict()
        self.__genres = dict()
        self.__score = 0.0
        self.__rank = 0
        self.__popularity = 0

        self._chapters = 0
        self._volumes = 0

        # staff from main content
        # staff from row 1
        self.__synopsis = ''

        # staff from row 2
        self.__adaptations = set()
        self.__characters = set()
        self.__sequels = set()
        self.__prequels = set()
        self.__spin_offs = set()
        self.__alternative_versions = set()
        self.__side_stories = set()
        self.__summaries = set()
        self.__others = set()
        self.__parent_stories = set()
        self.__alternative_settings = set()

        self.related_str_to_set_dict = {
            'Adaptation:': self.__adaptations,
            'Character:': self.__characters,
            'Sequel:': self.__sequels,
            'Prequel:': self.__prequels,
            'Spin-off:': self.__spin_offs,
            'Alternative version:': self.__alternative_versions,
            'Side story:': self.__side_stories,
            'Summary:': self.__summaries,
            'Other:': self.__others,
            'Parent story:': self.__parent_stories,
            'Alternative setting:': self.__alternative_settings,
        }

    @property
    def id(self) -> int:
        return self.__id

    @property
    @decorators.load
    def title(self) -> str:
        return self.__title

    @property
    @decorators.load
    def image_url(self) -> str:
        return self.__image_url

    def get_image(self) -> Image.Image:
        sock = requests.get(self.image_url)
        data = io.BytesIO(sock.content)
        return Image.open(data)

    @property
    @decorators.load
    def english(self) -> str:
        return self.__english

    @property
    @decorators.load
    def synonyms(self) -> str:
        return self.__synonyms

    @property
    @decorators.load
    def japanese(self) -> str:
        return self.__japanese

    @property
    @decorators.load
    def type(self) -> str:
        return self.__type

    @property
    @decorators.load
    def status(self) -> int:
        return self.__status

    @property
    @decorators.load
    def start_time(self) -> int:
        return self.__start_time

    @property
    @decorators.load
    def end_time(self) -> int:
        return self.__end_time

    @property
    @decorators.load
    def creators(self) -> dict:
        return self.__creators

    @property
    @decorators.load
    def genres(self) ->dict:
        return self.__genres

    @property
    @decorators.load
    def score(self) -> float:
        return self.__score

    @property
    @decorators.load
    def rank(self) -> int:
        return self.__rank

    @property
    @decorators.load
    def popularity(self) -> int:
        return self.__popularity

    @property
    @decorators.load
    def synopsis(self) -> str:
        return self.__synopsis

    # staff from main content
    @property
    @decorators.load
    def adaptations(self) -> frozenset:
        return frozenset(self.__adaptations)

    @property
    @decorators.load
    def characters(self) -> frozenset:
        return frozenset(self.__characters)

    @property
    @decorators.load
    def sequels(self) -> frozenset:
        return frozenset(self.__sequels)

    @property
    @decorators.load
    def prequels(self) -> frozenset:
        return frozenset(self.__prequels)

    @property
    @decorators.load
    def spin_offs(self) -> frozenset:
        return frozenset(self.__spin_offs)

    @property
    @decorators.load
    def alternative_versions(self) -> frozenset:
        return frozenset(self.__alternative_versions)

    @property
    @decorators.load
    def side_stories(self) -> frozenset:
        return frozenset(self.__side_stories)

    @property
    @decorators.load
    def summaries(self) -> frozenset:
        return frozenset(self.__summaries)

    @property
    @decorators.load
    def others(self) -> frozenset:
        return frozenset(self.__others)

    @property
    @decorators.load
    def parent_stories(self) -> frozenset:
        return frozenset(self.__parent_stories)

    @property
    @decorators.load
    def alternative_settings(self) -> frozenset:
        return frozenset(self.__alternative_settings)

    @property
    @decorators.load
    def volumes(self) -> int:
        return self.__volumes

    @property
    @decorators.load
    def chapters(self) -> int:
        return self.__chapters

    def reload(self):
        # Getting content wrapper <div>
        content_wrapper_div = global_functions.get_content_wrapper_div(self.__mal_url, global_functions.connect)

        # Getting title <div>
        self.__title = content_wrapper_div.h1.contents[1].strip()

        # Getting content <div>
        content_div = content_wrapper_div.find(
            name="div", attrs={"id": "content"}, recursive=False)
        if consts.DEBUG:
            assert content_div is not None

        content_table = content_div.table

        contents = content_table.tbody.tr.findAll(name="td", recursive=False)

        # Data from side content
        side_content = contents[0]
        side_contents_divs = side_content.findAll(name="div", recursive=False)

        # Getting manga image url <img>
        img_div = side_contents_divs[0]
        img_link = img_div.find(name="a")
        assert img_link is not None
        self.__image_url = img_link.img['src']

        side_contents_divs_index = 3

        # english <div>
        english_div = side_contents_divs[side_contents_divs_index]
        if global_functions.check_side_content_div('English', english_div):
            english_span, self_english = english_div.contents
            self.__english = self_english.strip()
            side_contents_divs_index += 1
        else:
            self.__english = ''

        # synonyms <div>
        synonyms_div = side_contents_divs[side_contents_divs_index]
        if global_functions.check_side_content_div('Synonyms', synonyms_div):
            synonyms_span, self_synonyms = synonyms_div.contents
            self.__synonyms = self_synonyms.strip()
            side_contents_divs_index += 1
        else:
            self.__synonyms = ''

        # japanese <div>
        japanese_div = side_contents_divs[side_contents_divs_index]
        if global_functions.check_side_content_div('Japanese', japanese_div):
            japanese_span, self_japanese = japanese_div.contents
            self.__japanese = self_japanese.strip()
            side_contents_divs_index += 1
        else:
            self.__japanese = ''

        # type <div>
        type_div = side_contents_divs[side_contents_divs_index]
        assert global_functions.check_side_content_div('Type', type_div)
        type_span, self_type = type_div.contents
        self.__type = self_type.strip()
        side_contents_divs_index += 1

        # volumes <div>
        volumes_div = side_contents_divs[side_contents_divs_index]
        assert global_functions.check_side_content_div('Volumes', volumes_div)
        volumes_span, self_volumes = volumes_div.contents
        self.__volumes = global_functions.make_counter(self_volumes.strip())
        side_contents_divs_index += 1

        # chapters <div>
        chapters_div = side_contents_divs[side_contents_divs_index]
        assert global_functions.check_side_content_div('Chapters', chapters_div)
        chapters_span, self_chapters = chapters_div.contents
        self.__chapters = global_functions.make_counter(self_chapters .strip())
        side_contents_divs_index += 1

        # status <div>
        status_div = side_contents_divs[side_contents_divs_index]
        assert global_functions.check_side_content_div('Status', status_div)
        status_span, self.__status = status_div.contents
        self.__status = self.__status.strip()
        side_contents_divs_index += 1

        # published <div>
        published_div = side_contents_divs[side_contents_divs_index]
        assert global_functions.check_side_content_div('Published', published_div)
        published_span, published = published_div.contents
        self.__start_time, self.__end_time = global_functions.make_start_and_end_time(published)
        side_contents_divs_index += 1

        # genres <div>
        genres_div = side_contents_divs[side_contents_divs_index]
        assert global_functions.check_side_content_div('Genres', genres_div)
        for genre_link in genres_div.findAll(name='a'):
            self.__genres[genre_link.text.strip()] = genre_link['href']
        side_contents_divs_index += 1

        # authors <div>
        authors_div = side_contents_divs[side_contents_divs_index]
        assert global_functions.check_side_content_div('Authors', authors_div)
        for authors_link in authors_div.findAll(name='a'):
            self.__creators[authors_link.text.strip()] = authors_link['href']
        side_contents_divs_index += 1

        side_contents_divs_index += 1

        # score <div>
        score_div = side_contents_divs[side_contents_divs_index]
        assert global_functions.check_side_content_div('Score', score_div)
        score_span, self_score = score_div.contents[:2]
        self.__score = float(self_score)
        side_contents_divs_index += 1

        # rank <div>
        rank_div = side_contents_divs[side_contents_divs_index]
        assert global_functions.check_side_content_div('Ranked', rank_div)
        rank_span, self_rank = rank_div.contents[:2]
        self_rank = self_rank.strip()
        assert self_rank.startswith("#")
        self.__rank = int(self_rank[1:])
        side_contents_divs_index += 1

        # popularity <div>
        popularity_div = side_contents_divs[side_contents_divs_index]
        assert global_functions.check_side_content_div('Popularity', popularity_div)
        popularity_span, self_popularity = popularity_div.contents[:2]
        self_popularity = self_popularity.strip()
        assert self_popularity.startswith("#")
        self.__popularity = int(self_popularity[1:])

        # Data from main content
        main_content = contents[1]
        main_content_inner_divs = main_content.findAll(
            name='div', recursive=False)
        if consts.DEBUG:
            assert 2 == len(main_content_inner_divs), \
                "Got len(main_content_inner_divs) == {0:d}".format(
                    len(main_content_inner_divs))
        main_content_datas = main_content_inner_divs[
            1].table.tbody.findAll(name="tr", recursive=False)

        synopsis_cell = main_content_datas[0]
        main_content_other_data = main_content_datas[1]

        # Getting synopsis
        synopsis_cell = synopsis_cell.td
        synopsis_cell_contents = synopsis_cell.contents
        if consts.DEBUG:
            assert 'Synopsis' == synopsis_cell.h2.text.strip(
            ), synopsis_cell.h2.text.strip()
        self.__synopsis = os.linesep.join([
            synopsis_cell_content.strip()
            for synopsis_cell_content in synopsis_cell_contents[1:-1]
            if isinstance(synopsis_cell_content, bs4.element.NavigableString)
        ])

        # Getting other data
        main_content_other_data = main_content_other_data.td
        other_data_kids = [i for i in main_content_other_data.children]

        # Getting all the data under 'Related Manga'
        index = 0
        index = global_functions.get_next_index(index, other_data_kids)
        if 'h2' == other_data_kids[index].name and\
           'Related Manga' == other_data_kids[index].text.strip():
            index += 1
            while other_data_kids[index + 1].name != 'br':
                index = global_functions.make_set(
                    self.related_str_to_set_dict[
                        other_data_kids[index].strip()],
                    index, other_data_kids)
        else:
            index -= 2
        next_index = global_functions.get_next_index(index, other_data_kids)

        if consts.DEBUG:
            assert next_index - \
                index == 2, "{0:d} - {1:d}".format(next_index, index)
            index = next_index + 1

            # Getting all the data under 'Characters & Voice Actors'
            assert 'h2' == other_data_kids[index].name, 'h2 == {0:s}'.format(
                other_data_kids[index].name)
            assert 'Characters' == other_data_kids[index].contents[-1],\
                other_data_kids[index].contents[-1]

        self._is_loaded = True

    @property
    def MY_MAL_XML_TEMPLATE(self):
        return """<?xml version="1.0" encoding="UTF-8"?>
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

    def add(self, account):
        """
        """
        data = self.MY_MAL_XML_TEMPLATE.format(
            0, 0, 6, 0, 0, 0, 0, consts.MALAPI_NONE_TIME,
            consts.MALAPI_NONE_TIME, 0, False, False, '', '', '', 0
        )
        xml = ''.join(map(lambda x: x.strip(), data.splitlines()))
        delete_url = self.__MY_MAL_ADD_URL.format(self.id)
        ret = account.auth_connect(
            delete_url,
            data='data=' + xml,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        if not ret.isdigit():
            raise exceptions.MyAnimeListApiAddError(ret)
        my_id = int(ret)

        from pymal.account_objects import MyManga
        return MyManga.MyManga(self, my_id, account)

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
        hash_md5.update(b'Manga')
        return int(hash_md5.hexdigest(), 16)

    def __repr__(self):
        title = '' if self.__title is None else ' ' + self.__title
        return "<{0:s}{1:s} id={2:d}>".format(self.__class__.__name__, title,
                                              self.__id)
