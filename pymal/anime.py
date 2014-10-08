__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

from urllib import request
import os
import io
import hashlib

from PIL import Image
import requests
import bs4
import singleton_factory
from reloaded_set import load

from pymal import consts
from pymal import global_functions
from pymal import exceptions

__all__ = ['Anime']


class Anime(object, metaclass=singleton_factory.SingletonFactory):
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
    :ivar episodes: :class:`int`
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
    :ivar full_stories: :class:`frozenset`
    """

    __GLOBAL_MAL_URL = request.urljoin(consts.HOST_NAME, "anime/{0:d}")
    __MY_MAL_ADD_URL = request.urljoin(
        consts.HOST_NAME, 'api/animelist/add/{0:d}.xml')

    def __init__(self, mal_id: int):
        """
        :param mal_id: the anime id in mal.
        :type mal_id: int
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
        self.__duration = 0
        self.__score = 0.0
        self.__rank = 0
        self.__popularity = 0

        self.__rating = ''
        self.__episodes = 0

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
        self.__full_stories = set()

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
            'Full story:': self.__full_stories,
            }

    @property
    def id(self) -> int:
        """
        :return: The anime's id.
        :rtype: :class:`int`
        """
        return self.__id

    @property
    @load()
    def title(self) -> str:
        return self.__title

    @property
    @load()
    def image_url(self) -> str:
        return self.__image_url

    def get_image(self):
        """
        :return: The anime's image.
        :rtype: :class:`PIL.Image.Image`
        """
        sock = requests.get(self.image_url)
        data = io.BytesIO(sock.content)
        return Image.open(data)

    @property
    @load()
    def english(self) -> str:
        return self.__english

    @property
    @load()
    def synonyms(self) -> str:
        return self.__synonyms

    @property
    @load()
    def japanese(self) -> str:
        return self.__japanese

    @property
    @load()
    def type(self) -> str:
        return self.__type

    @property
    @load()
    def status(self) -> int:
        return self.__status

    @property
    @load()
    def start_time(self) -> int:
        return self.__start_time

    @property
    @load()
    def end_time(self) -> int:
        return self.__end_time

    @property
    @load()
    def creators(self) -> dict:
        return self.__creators

    @property
    @load()
    def genres(self) -> dict:
        return self.__genres

    @property
    @load()
    def duration(self) -> int:
        return self.__duration

    @property
    @load()
    def score(self) -> float:
        return self.__score

    @property
    @load()
    def rank(self) -> int:
        return self.__rank

    @property
    @load()
    def popularity(self) -> int:
        return self.__popularity

    @property
    @load()
    def synopsis(self) -> str:
        return self.__synopsis

    # staff from main content
    @property
    @load()
    def adaptations(self) -> frozenset:
        return frozenset(self.__adaptations)

    @property
    @load()
    def characters(self) -> frozenset:
        return frozenset(self.__characters)

    @property
    @load()
    def sequels(self) -> frozenset:
        return frozenset(self.__sequels)

    @property
    @load()
    def prequels(self) -> frozenset:
        return frozenset(self.__prequels)

    @property
    @load()
    def spin_offs(self) -> frozenset:
        return frozenset(self.__spin_offs)

    @property
    @load()
    def alternative_versions(self) -> frozenset:
        return frozenset(self.__alternative_versions)

    @property
    @load()
    def side_stories(self) -> frozenset:
        return frozenset(self.__side_stories)

    @property
    @load()
    def summaries(self) -> frozenset:
        return frozenset(self.__summaries)

    @property
    @load()
    def others(self) -> frozenset:
        return frozenset(self.__others)

    @property
    @load()
    def parent_stories(self) -> frozenset:
        return frozenset(self.__parent_stories)

    @property
    @load()
    def alternative_settings(self) -> frozenset:
        return frozenset(self.__alternative_settings)

    @property
    @load()
    def full_stories(self) -> frozenset:
        return frozenset(self.__full_stories)

    @property
    @load()
    def rating(self) -> int:
        return self.__rating

    @property
    @load()
    def episodes(self) -> int:
        return self.__episodes

    def _synopsis_bar(self, synopsis_cell: bs4.element.Tag):
        """
        :param synopsis_cell: synopsis tag
        :type synopsis_cell: bs4.element.Tag
        :exception exceptions.FailedToReloadError: If failed to parse.
        """
        synopsis_cell = synopsis_cell.td
        synopsis_cell_contents = synopsis_cell.contents
        if 'Synopsis' != synopsis_cell.h2.text.strip():
            raise exceptions.FailedToReloadError(synopsis_cell.h2.text.strip())
        self.__synopsis = os.linesep.join([
            synopsis_cell_content.strip()
            for synopsis_cell_content in synopsis_cell_contents[1:-1]
            if isinstance(synopsis_cell_content, bs4.element.NavigableString)
        ])

    def _main_bar(self, main_content: bs4.element.Tag):
        """
        :param main_content: The main content.
        :type main_content: bs4.element.Tag
        :exception exceptions.FailedToReloadError: If failed to parse.
        """
        main_content_inner_divs = main_content.findAll(
            name='div', recursive=False)
        if 2 != len(main_content_inner_divs):
            raise exceptions.FailedToReloadError(
                "Got len(main_content_inner_divs) == {0:d}".format(
                    len(main_content_inner_divs)))
        main_content_datas = main_content_inner_divs[
            1].table.tbody.findAll(name="tr", recursive=False)

        self._synopsis_bar(main_content_datas[0])

        main_content_other_data = main_content_datas[1]
        # Getting other data
        main_content_other_data = main_content_other_data.td
        other_data_kids = [i for i in main_content_other_data.children]
        # Getting all the data under 'Related Anime'
        index = 0
        index = global_functions.get_next_index(index, other_data_kids)
        if 'h2' == other_data_kids[index].name and 'Related Anime' == other_data_kids[index].text.strip():
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
            if next_index - index != 2:
                raise exceptions.FailedToReloadError("{0:d} - {1:d}".format(next_index, index))
            index = next_index + 1

            # Getting all the data under 'Characters & Voice Actors'
            if 'h2' != other_data_kids[index].name:
                raise exceptions.FailedToReloadError('h2 == {0:s}'.format(other_data_kids[index].name))
            if 'Characters & Voice Actors' != other_data_kids[index].contents[-1]:
                raise exceptions.FailedToReloadError(other_data_kids[index].contents[-1])
        tag_for_reviews = main_content_other_data.find(text='More reviews').parent
        link_for_reviews = request.urljoin(consts.HOST_NAME, tag_for_reviews['href'])
        self.__parse_reviews(link_for_reviews)
        tag_for_recommendations = main_content_other_data.find(text='More recommendations').parent
        link_for_recommendations = request.urljoin(consts.HOST_NAME, tag_for_recommendations['href'])
        self.__parse_recommendations(link_for_recommendations)

    def _image_parse(self, img_div: bs4.element.Tag):
        """
        Getting image url <img>.
        :param img_div: image div
        :type img_div: bs4.element.Tag
        """
        img_link = img_div.find(name="a")
        if img_link is None:
            raise exceptions.FailedToReloadError(img_div)
        self.__image_url = img_link.img['src']
        return 1

    def _english_parse(self, english_div):
        """
        english <div>
        :param english_div: potent english div
        :type english_div: bs4.element.Tag
        :return: 1 if was found, otherwise 0.
        """
        if global_functions.check_side_content_div('English', english_div):
            english_span, self_english = english_div.contents
            self.__english = self_english.strip()
            return 1
        else:
            self.__english = ''
            return 0

    def _synonyms_parse(self, synonyms_div: bs4.element.Tag):
        """
        synonyms <div>
        :param synonyms_div: potent synonyms div
        :type synonyms_div: bs4.element.Tag
        :return: 1 if was found, otherwise 0.
        """
        if global_functions.check_side_content_div('Synonyms', synonyms_div):
            synonyms_span, self_synonyms = synonyms_div.contents
            self.__synonyms = self_synonyms.strip()
            return 1
        else:
            self.__synonyms = ''
            return 0

    def _japanese_parse(self, japanese_div: bs4.element.Tag):
        """
        japanese <div>
        :param japanese_div: potent japanese div
        :type japanese_div: bs4.element.Tag
        :return: 1 if was found, otherwise 0.
        """
        if global_functions.check_side_content_div('Japanese', japanese_div):
            japanese_span, self_japanese = japanese_div.contents
            self.__japanese = self_japanese.strip()
            return 1
        else:
            self.__japanese = ''
            return 0

    def _type_parse(self, type_div: bs4.element.Tag):
        """
        :param type_div: type div
        :type type_div: bs4.element.Tag
        :return: 1.
        """
        if not global_functions.check_side_content_div('Type', type_div):
            raise exceptions.FailedToReloadError(type_div)
        type_span, self_type = type_div.contents
        self.__type = self_type.strip()
        return 1

    def _status_parse(self, status_div: bs4.element.Tag):
        """
        :param status_div: Status div
        :type status_div: bs4.element.Tag
        :return: 1.
        """
        if not global_functions.check_side_content_div('Status', status_div):
            raise exceptions.FailedToReloadError(status_div)
        status_span, self.__status = status_div.contents
        self.__status = self.__status.strip()
        return 1

    def _genres_parse(self, genres_div: bs4.element.Tag):
        """
        :param genres_div: Genres <div>
        :type genres_div: bs4.element.Tag
        :return: 1.
        """
        if not global_functions.check_side_content_div('Genres', genres_div):
            raise exceptions.FailedToReloadError(genres_div)
        for genre_link in genres_div.findAll(name='a'):
            self.__genres[genre_link.text.strip()] = genre_link['href']
        return 1

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

    def _aired_parse(self, aired_div: bs4.element.Tag):
        """
        :param aired_div: Aired <div>
        :type aired_div: bs4.element.Tag
        :return: 1.
        """
        if not global_functions.check_side_content_div('Aired', aired_div):
            raise exceptions.FailedToReloadError(aired_div)
        aired_span, aired = aired_div.contents
        self.__start_time, self.__end_time = global_functions.make_start_and_end_time(aired)
        return 1

    def _producers_parse(self, producers_div: bs4.element.Tag):
        """
        :param producers_div: Aired <div>
        :type producers_div: bs4.element.Tag
        :return: 1.
        """
        if not global_functions.check_side_content_div('Producers', producers_div):
            raise exceptions.FailedToReloadError(producers_div)
        for producer_link in producers_div.findAll(name='a'):
            self.__creators[producer_link.text.strip()] = producer_link['href']
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

    def _rank_parse(self, rank_div: bs4.element.Tag):
        """
        :param rank_div: Rank <div>
        :type rank_div: bs4.element.Tag
        :return: 1.
        """
        if not global_functions.check_side_content_div('Ranked', rank_div):
            raise exceptions.FailedToReloadError(rank_div)
        rank_span, self_rank = rank_div.contents[:2]
        self_rank = self_rank.strip()
        if not self_rank.startswith("#"):
            raise exceptions.FailedToReloadError(self_rank)
        self.__rank = int(self_rank[1:])
        return 1

    def _score_parse(self, score_div: bs4.element.Tag):
        """
        :param score_div: Score <div>
        :type score_div: bs4.element.Tag
        :return: 1.
        """
        if not global_functions.check_side_content_div('Score', score_div):
            raise exceptions.FailedToReloadError(score_div)
        score_span, self_score = score_div.contents[:2]
        self.__score = float(self_score)
        return 1

    def _popularity_parse(self, popularity_div: bs4.element.Tag):
        """
        :param popularity_div: Popularity <div>
        :type popularity_div: bs4.element.Tag
        :return: 1.
        """
        if not global_functions.check_side_content_div('Popularity', popularity_div):
            raise exceptions.FailedToReloadError(popularity_div)
        popularity_span, self_popularity = popularity_div.contents[:2]
        self_popularity = self_popularity.strip()
        if not self_popularity.startswith("#"):
            raise exceptions.FailedToReloadError(self_popularity)
        self.__popularity = int(self_popularity[1:])
        return 1

    def _void_parse(self, div: bs4.element.Tag):
        """
        :param div: A <div>
        :type div: bs4.element.Tag
        :return: 1.
        """
        return 1

    def _side_bar(self, side_content: bs4.element.Tag):
        """
        :param side_content: The side bar content
        :type side_content: bs4.element.Tag
        :exception exceptions.FailedToReloadError: If failed to parse.
        """
        side_contents_divs = side_content.findAll(name="div", recursive=False)

        parser = [
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
            self._aired_parse,
            self._producers_parse,
            self._genres_parse,
            self._duration_parse,
            self._rating_parse,
            self._score_parse,
            self._rank_parse,
            self._popularity_parse
        ]

        index = 0

        for function in parser:
            index += function(side_contents_divs[index])

    def reload(self):
        """
        :exception exceptions.FailedToReloadError: when failed.
        """
        # Getting content wrapper <div>
        content_wrapper_div = global_functions.get_content_wrapper_div(self.__mal_url, global_functions.connect)

        # Getting title <div>
        self.__title = content_wrapper_div.h1.contents[1].strip()

        # Getting content <div>
        content_div = content_wrapper_div.find(
            name="div", attrs={"id": "content"}, recursive=False)

        if content_div is None:
            raise exceptions.FailedToReloadError(content_wrapper_div)

        content_table = content_div.table

        contents = content_table.tbody.tr.findAll(name="td", recursive=False)

        # Data from side content
        self._side_bar(contents[0])

        # Data from main content
        self._main_bar(contents[1])

        self._is_loaded = True

    def __parse_reviews(self, link_for_reviews: str):
        from pymal.inner_objects import review

        content_wrapper_div = global_functions.get_content_wrapper_div(link_for_reviews, global_functions.connect)
        content_div = content_wrapper_div.find(name="div", attrs={"id": "content"}, recursive=False)
        _, main_cell = content_div.table.tbody.tr.findAll(name='td', recursive=False)
        _, reviews_data_div = main_cell.findAll(name='div', recursive=False)
        reviews_data = reviews_data_div.findAll(name='div', recursive=False)[2:-2]
        self.reviews = frozenset(map(review.Review, reviews_data))

    def __parse_recommendations(self, link_for_recommendations: str):
        from pymal.inner_objects import recommendation

        content_wrapper_div = global_functions.get_content_wrapper_div(link_for_recommendations,
                                                                       global_functions.connect)
        content_div = content_wrapper_div.find(name="div", attrs={"id": "content"}, recursive=False)
        _, main_cell = content_div.table.tbody.tr.findAll(name='td', recursive=False)
        _, recommendations_data_div = main_cell.findAll(name='div', recursive=False)
        recommendations_data = recommendations_data_div.findAll(name='div', recursive=False)[2:-1]
        self.recommendations = frozenset(map(recommendation.Recommendation, recommendations_data))

    @property
    def MY_MAL_XML_TEMPLATE(self) -> str:
        return """<?xml version="1.0" encoding="UTF-8"?>
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

    def add(self, account):
        """
        :param account: the account to add him self anime.
        :type account: :class:`account.Account`
        :rtype: :class:`account_objects.my_anime.MyAnime`
        :exception exceptions.MyAnimeListApiAddError: when failed.
        """
        data = self.MY_MAL_XML_TEMPLATE.format(
            0, 6, 0, 0, 0, 0, 0, 0, consts.MALAPI_NONE_TIME,
            consts.MALAPI_NONE_TIME, 0, False, False, '', '', ''
        )
        xml = ''.join(map(lambda x: x.strip(), data.splitlines()))
        delete_url = self.__MY_MAL_ADD_URL.format(self.id)
        ret = account.auth_connect(
            delete_url,
            data='data=' + xml,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        try:
            html_obj = bs4.BeautifulSoup(ret)
            if html_obj is None:
                raise exceptions.FailedToAddError(html_obj)

            head_obj = html_obj.head
            if head_obj is None:
                raise exceptions.FailedToAddError(head_obj)

            title_obj = head_obj.title
            if title_obj is None:
                raise exceptions.FailedToAddError(title_obj)

            data = title_obj.text
            if data is None:
                raise exceptions.FailedToAddError(data)

            my_id, string = data.split()
            if not my_id.isdigit():
                raise exceptions.FailedToAddError(my_id)
            if string != 'Created':
                raise exceptions.FailedToAddError(string)
        except exceptions.FailedToAddError:
            raise exceptions.MyAnimeListApiAddError(ret)

        from pymal.account_objects import my_anime

        return my_anime.MyAnime(self, my_id, account)

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
        hash_md5.update(b'Anime')
        return int(hash_md5.hexdigest(), 16)

    def __repr__(self):
        title = '' if self.__title is None else ' ' + self.__title
        return "<{0:s}{1:s} id={2:d}>".format(self.__class__.__name__, title,
                                              self.__id)

    def __format__(self, format_spec):
        return str(self).__format__(format_spec)
