from urllib import request
from pymal.consts import HOST_NAME, DEBUG, SITE_PUBLISHED_FORMAT_TIME, MALAPPINFO_FORMAT_TIME
from pymal.decorators import load
from pymal.MALObject import MALObject, check_side_content_div
from pymal.global_functions import connect, make_list, get_next_index
import time


class Manga(MALObject):
    MANGA_URL = request.urljoin(HOST_NAME, "manga/{0:d}")

    def __init__(self, manga_id: int, manga_xml=None):
        self._manga_id = manga_id
        self._is_loaded = False

        self.__manga_url = self.MANGA_URL.format(self._manga_id)

        ### Getting staff from html
        ## staff from side content
        self.__title = None
        self.__image_url = None
        self.__english = ''
        self.__synonyms = None
        self.__japanese = ''
        self.__type = None
        self.__volumes = None
        self.__chapters = None
        self.__status = None
        self.__start_time = None
        self.__end_time = None
        self.__authors = dict()
        self.__genres = dict()
        self.__rating = 0
        self.__score = 0.0
        self.__rank = 0
        self.__popularity = 0

        ## staff from main content
        #staff from row 1
        self.__synopsis = ''

        #staff from row 2
        self.__adaptations = list()
        self.__characters = list()
        self.__sequals = list()
        self.__prequel = list()
        self.__spin_offs = list()
        self.__alternative_versions = list()
        self.__side_story = list()
        self.__summary = list()
        self.__other = list()
        self.__parent_story = list()
        self.__alternative_setting = list()

        if manga_xml is not None:
            self.__title = manga_xml.find('series_title').text.strip()
            self.__synonyms = manga_xml.find('series_synonyms').text
            if self.__synonyms is not None:
                self.__synonyms = self.__synonyms.strip()
            # TODO: make this number to a string (or the string to a number?)
            self.__type = manga_xml.find('series_type').text.strip()
            self.__episodes = int(manga_xml.find('series_chapters').text.strip())
            self.__volumes = int(manga_xml.find('series_volumes').text.strip())
            try:
                self.__status = int(manga_xml.find('series_status').text.strip())
            except ValueError:
                self.__status = manga_xml.find('series_status').text.strip()
                print('self.__status=', self.__status)
            start_time = manga_xml.find('series_start').text.strip()
            if start_time == '0000-00-00':
                self.__start_time = float('inf')
            else:
                start_time = start_time[:4] + start_time[4:].replace('00', '01')
                self.__start_time = time.mktime(time.strptime(start_time, MALAPPINFO_FORMAT_TIME))
            end_time = manga_xml.find('series_end').text.strip()
            if end_time == '0000-00-00':
                self.__end_time = float('inf')
            else:
                end_time = end_time[:4] + end_time[4:].replace('00', '01')
                self.__end_time = time.mktime(time.strptime(end_time, MALAPPINFO_FORMAT_TIME))
            self.__image_url = manga_xml.find('series_image').text.strip()

    @property
    def id(self):
        return self._manga_id

    @property
    def title(self):
        if self.__title is None:
            self.reload()
        return self.__title

    @property
    def image_url(self):
        if self.__image_url is None:
            self.reload()
        return self.__image_url

    @property
    @load
    def english(self):
        return self.__english

    @property
    def synonyms(self):
        if self.__synonyms is None:
            self.reload()
        return self.__synonyms

    @property
    @load
    def japanese(self):
        return self.__japanese

    @property
    def type(self):
        if self.__type is None:
            self.reload()
        return self.__type

    @property
    def volumes(self):
        if self.__volumes is None:
            self.reload()
        return self.__volumes

    @property
    def chapters(self):
        if self.__chapters is None:
            self.reload()
        return self.__chapters

    @property
    def status(self):
        if self.__status is None:
            self.reload()
        return self.__status

    @property
    def start_time(self):
        if self.__start_time is None:
            self.reload()
        return self.__start_time

    @property
    def end_time(self):
        if self.__end_time is None:
            self.reload()
        return self.__end_time

    @property
    @load
    def authors(self):
        return self.__authors

    @property
    @load
    def genres(self):
        return self.__genres

    @property
    @load
    def rating(self):
        return self.__rating

    @property
    @load
    def score(self):
        return self.__score

    @property
    @load
    def rank(self):
        return self.__rank

    @property
    @load
    def popularity(self):
        return self.__popularity

    @property
    @load
    def synopsis(self):
        return self.__synopsis

    # staff from main content
    @property
    @load
    def adaptations(self):
        return self.__adaptations

    @property
    @load
    def characters(self):
        return self.__characters

    @property
    @load
    def sequals(self):
        return self.__sequals

    @property
    @load
    def prequel(self):
        return self.__prequel

    @property
    @load
    def spin_offs(self):
        return self.__spin_offs

    @property
    @load
    def alternative_versions(self):
        return self.__alternative_versions

    @property
    @load
    def side_story(self):
        return self.__side_story

    @property
    @load
    def summary(self):
        return self.__summary

    @property
    @load
    def other(self):
        return self.__other

    @property
    @load
    def parent_story(self):
        return self.__parent_story

    @property
    @load
    def alternative_setting(self):
        return self.__alternative_setting

    def reload(self):
        # Getting content wrapper <div>
        content_wrapper_div = self._get_content_wrapper_div(self.__manga_url, connect)

        # Getting title <div>
        self.__title = content_wrapper_div.h1.contents[1].strip()

        #Getting content <div>
        content_div = content_wrapper_div.find(name="div", attrs={"id": "content"}, recursive=False)
        if DEBUG:
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

        side_contents_divs_index = 4
        # english <div>
        english_div = side_contents_divs[side_contents_divs_index]
        if check_side_content_div('English', english_div):
            english_span, self.__english = english_div.contents
            self.__english = self.__english.strip()
            side_contents_divs_index += 1

        # synonyms <div>
        synonyms_div = side_contents_divs[side_contents_divs_index]
        if check_side_content_div('Synonyms', synonyms_div):
            synonyms_span, self.__synonyms = synonyms_div.contents
            self.__synonyms = self.__synonyms.strip()
            side_contents_divs_index += 1

        # japanese <div>
        japanese_div = side_contents_divs[side_contents_divs_index]
        if check_side_content_div('Japanese', japanese_div):
            japanese_span, self.__japanese = japanese_div.contents
            self.__japanese = self.__japanese.strip()
            side_contents_divs_index += 1

        # type <div>
        type_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Type', type_div)
        type_span, self.__type = type_div.contents
        self.__type = self.__type.strip()
        side_contents_divs_index += 1

        # volumes <div>
        volumes_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Volumes', volumes_div)
        volumes_span, self_volumes = volumes_div.contents
        self_volumes = self_volumes.strip()
        if self_volumes.isdigit():
            self.__volumes = int(self_volumes)
        side_contents_divs_index += 1

        # chapters <div>
        chapters_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Chapters', chapters_div)
        chapters_span, self_chapters = chapters_div.contents
        if self_chapters.isdigit():
            self.__chapters = int(self_chapters)
        side_contents_divs_index += 1

        # status <div>
        status_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Status', status_div)
        status_span, self.__status = status_div.contents
        self.__status = self.__status.strip()
        side_contents_divs_index += 1

        # published <div>
        published_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Published', published_div)
        published_span, published = published_div.contents
        start_time, end_time = published.split('to')
        start_time, end_time = start_time.strip(), end_time.strip()
        if '?' == start_time:
            self.__start_time = float('inf')
        else:
            self.__start_time = time.mktime(time.strptime(start_time, SITE_PUBLISHED_FORMAT_TIME))
        if '?' == end_time:
            self.__end_time = float('inf')
        else:
            self.__end_time = time.mktime(time.strptime(end_time, SITE_PUBLISHED_FORMAT_TIME))
        side_contents_divs_index += 1

        # genres <div>
        genres_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Genres', genres_div)
        for genre_link in genres_div.findAll(name='a'):
            self.__genres[genre_link.text.strip()] = genre_link['href']
        side_contents_divs_index += 1

        # authors <div>
        authors_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Authors', authors_div)
        for authors_link in authors_div.findAll(name='a'):
            self.__authors[authors_link.text.strip()] = authors_link['href']
        side_contents_divs_index += 1

        side_contents_divs_index += 1

        # score <div>
        score_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Score', score_div)
        score_span, self_score = score_div.contents[:2]
        self.__score = float(self_score.strip())
        side_contents_divs_index += 1

        # rank <div>
        rank_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Ranked', rank_div)
        rank_span, self_rank = rank_div.contents[:2]
        self_rank = self_rank.strip()
        assert self_rank.startswith("#")
        self.__rank = int(self_rank[1:])
        side_contents_divs_index += 1

        # popularity <div>
        popularity_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Popularity', popularity_div)
        popularity_span, self_popularity = popularity_div.contents[:2]
        self_popularity = self_popularity.strip()
        assert self_popularity.startswith("#")
        self.__popularity = int(self_popularity[1:])

        # Data from main content
        main_content = contents[1]
        main_content_inner_divs = main_content.findAll(name='div', recursive=False)
        if DEBUG:
            assert 2 == len(main_content_inner_divs), \
                "Got len(main_content_inner_divs) == {0:d}".format(len(main_content_inner_divs))
        main_content_datas = main_content_inner_divs[1].table.tbody.findAll(name="tr", recursive=False)

        synopsis_cell = main_content_datas[0]
        main_content_other_data = main_content_datas[1]

        # Getting synopsis
        synopsis_cell = synopsis_cell.td
        synopsis_cell_contents = synopsis_cell.contents
        if DEBUG:
            assert 'Synopsis' == synopsis_cell.h2.text.strip(), synopsis_cell.h2.text.strip()
        self.__synopsis = synopsis_cell_contents[1]

        # Getting other data
        main_content_other_data = main_content_other_data.td
        other_data_kids = [i for i in main_content_other_data.children]

        # Getting all the data under 'Related Manga'
        related_str_to_list_dict = {
            'Adaptation:': self.__adaptations,
            'Character:': self.__characters,
            'Sequel:': self.__sequals,
            'Prequel:': self.__prequel,
            'Spin-off:': self.__spin_offs,
            'Alternative version:': self.__alternative_versions,
            'Side story:': self.__side_story,
            'Summary:': self.__summary,
            'Other:': self.__other,
            'Parent story:': self.__parent_story,
            'Alternative setting:': self.__alternative_setting,
        }

        index = 0
        index = get_next_index(index, other_data_kids)
        if 'h2' == other_data_kids[index].name and 'Related Manga' == other_data_kids[index].text.strip():
            index += 1
            while other_data_kids[index + 1].name != 'br':
                index = make_list(related_str_to_list_dict[other_data_kids[index].strip()], index, other_data_kids)
        else:
            index -= 2
        next_index = get_next_index(index, other_data_kids)

        if DEBUG:
            assert next_index - index == 2, "{0:d} - {1:d}".format(next_index, index)
            index = next_index + 1

            # Getting all the data under 'Characters & Voice Actors'
            assert 'h2' == other_data_kids[index].name, 'h2 == {0:s}'.format(other_data_kids[index].name)
            assert 'Characters' == other_data_kids[index].contents[-1], 'Characters == {0:s}'.format(other_data_kids[index].contents[-1])

        self._is_loaded = True

    def __repr__(self):
        return "<{0:s} id={1:d}>".format(self.__class__.__name__, self._manga_id)