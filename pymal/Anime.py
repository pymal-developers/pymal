from urllib import request
from pymal.consts import HOST_NAME, DEBUG, SITE_FORMAT_TIME, MALAPPINFO_FORMAT_TIME
from pymal.decorators import load
from pymal.MALObject import MALObject, check_side_content_div
from pymal.global_functions import connect, make_list, get_next_index
import os
from bs4.element import NavigableString
import time


class Anime(MALObject):
    GLOBAL_MAL_URL = request.urljoin(HOST_NAME, "anime/{0:d}")

    MY_MAL_ADD_URL = request.urljoin(HOST_NAME, 'api/animelist/add/{0:d}.xml')

    def __init__(self, anime_id: int, anime_xml=None):
        super().__init__()

        self._id = anime_id
        self._is_loaded = False

        self.__mal_url = self.GLOBAL_MAL_URL.format(self._id)

        ### Getting staff from html
        ## staff from side content
        self.__episodes = None

        if anime_xml is not None:
            self.__title = anime_xml.find('series_title').text.strip()
            self.__synonyms = anime_xml.find('series_synonyms').text
            if self.__synonyms is not None:
                self.__synonyms = self.__synonyms.strip()
            # TODO: make this number to a string (or the string to a number?)
            self.__type = anime_xml.find('series_type').text.strip()
            self.__episodes = int(anime_xml.find('series_episodes').text.strip())
            try:
                self.__status = int(anime_xml.find('series_status').text.strip())
            except ValueError:
                self.__status = anime_xml.find('series_status').text.strip()
                print('self.__status=', self.__status)
            start_time = anime_xml.find('series_start').text.strip()
            if start_time == '0000-00-00':
                self.__start_time = float('inf')
            else:
                start_time = start_time[:4] + start_time[4:].replace('00', '01')
                self.__start_time = time.mktime(time.strptime(start_time, MALAPPINFO_FORMAT_TIME))
            end_time = anime_xml.find('series_end').text.strip()
            if end_time == '0000-00-00':
                self.__end_time = float('inf')
            else:
                end_time = end_time[:4] + end_time[4:].replace('00', '01')
                self.__end_time = time.mktime(time.strptime(end_time, MALAPPINFO_FORMAT_TIME))
            self.__image_url = anime_xml.find('series_image').text.strip()

    @property
    def episodes(self):
        if self.__episodes is None:
            self.reload()
        return self.__episodes

    def reload(self):
        # Getting content wrapper <div>
        content_wrapper_div = self._get_content_wrapper_div(self.__mal_url, connect)

        # Getting title <div>
        rank_div, self.__title = content_wrapper_div.h1.contents

        #Getting content <div>
        content_div = content_wrapper_div.find(name="div", attrs={"id": "content"}, recursive=False)
        if DEBUG:
            assert content_div is not None

        content_table = content_div.table

        contents = content_table.tbody.tr.findAll(name="td", recursive=False)

        # Data from side content
        side_content = contents[0]
        side_contents_divs = side_content.findAll(name="div", recursive=False)

        # Getting anime image url <img>
        img_div = side_contents_divs[0]
        img_link = img_div.find(name="a")
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

        # episodes <div>
        episodes_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Episodes', episodes_div)
        episodes_span, self_episodes = episodes_div.contents
        if 'Unknown' == self_episodes.strip():
            self.__episodes = float('inf')
        else:
            self.__episodes = int(self_episodes.strip())
        side_contents_divs_index += 1

        # status <div>
        status_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Status', status_div)
        status_span, self.__status = status_div.contents
        self.__status = self.__status.strip()
        side_contents_divs_index += 1

        # aired <div>
        aired_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Aired', aired_div)
        aired_span, aired = aired_div.contents
        start_time, end_time = aired.split('to')
        start_time, end_time = start_time.strip(), end_time.strip()
        self.__start_time = time.mktime(time.strptime(start_time, SITE_FORMAT_TIME))
        self.__end_time = time.mktime(time.strptime(end_time, SITE_FORMAT_TIME))
        side_contents_divs_index += 1

        # producers <div>
        producers_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Producers', producers_div)
        for producer_link in producers_div.findAll(name='a'):
            self.__creators[producer_link.text.strip()] = producer_link['href']
        side_contents_divs_index += 1

        # genres <div>
        genres_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Genres', genres_div)
        for genre_link in genres_div.findAll(name='a'):
            self.__genres[genre_link.text.strip()] = genre_link['href']
        side_contents_divs_index += 1

        side_contents_divs_index += 1

        # rating <div>
        rating_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Rating', rating_div)
        rating_span, self.__rating = rating_div.contents
        self.__rating = self.__rating.strip()
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
        assert 2 == len(main_content_datas), \
            "Got len(main_content_datas) == {0:d}".format(len(main_content_datas))

        synopsis_cell, main_content_other_data = main_content_datas

        # Getting synopsis
        synopsis_cell = synopsis_cell.td
        synopsis_cell_contents = synopsis_cell.contents
        if DEBUG:
            assert 'Synopsis' == synopsis_cell.h2.text.strip(), synopsis_cell.h2.text.strip()
        self.__synopsis = os.linesep.join([synopsis_cell_content.strip() for synopsis_cell_content in synopsis_cell_contents[1:-1] if type(synopsis_cell_content) == NavigableString])

        # Getting other data
        main_content_other_data = main_content_other_data.td
        other_data_kids = [i for i in main_content_other_data.children]

        # Getting all the data under 'Related Anime'
        #related_str_to_list_dict = {
        #    'Adaptation:': self.__adaptations,
        #    'Character:': self.__characters,
        #    'Sequel:': self.__sequals,
        #    'Prequel:': self.__prequel,
        #    'Spin-off:': self.__spin_offs,
        #    'Alternative version:': self.__alternative_versions,
        #    'Side story:': self.__side_stories,
        #    'Summary:': self.__summaries,
        #    'Other:': self.__others,
        #    'Parent story:': self.__parent_stories,
        #    'Alternative setting:': self.__alternative_settings,
        #}

        index = 0
        index = get_next_index(index, other_data_kids)
        if 'h2' == other_data_kids[index].name and 'Related Anime' == other_data_kids[index].text.strip():
            index += 1
            while other_data_kids[index + 1].name != 'br':
                index = make_list(self.related_str_to_list_dict[other_data_kids[index].strip()], index, other_data_kids)
        else:
            index -= 2
        next_index = get_next_index(index, other_data_kids)

        if DEBUG:
            assert next_index - index == 2, "{0:d} - {1:d}".format(next_index, index)
            index = next_index + 1

            # Getting all the data under 'Characters & Voice Actors'
            assert 'h2' == other_data_kids[index].name, other_data_kids[index].name
            assert 'Characters & Voice Actors' == other_data_kids[index].contents[-1], other_data_kids[index].contents[-1]

        self._is_loaded = True

    def __eq__(self, other):
        if not issubclass(Anime, other):
            return False
        return self._id == other._id
