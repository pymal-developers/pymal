from urllib import request
from consts import HOST_NAME, DEBUG
from decorators import load
from MALObject import MALObject, check_side_content_div
from global_functions import connect, make_list, get_next_index


class Anime(MALObject):
    ANIME_URL = request.urljoin(HOST_NAME, "anime/{0:d}")

    def __init__(self, anime_id: int):
        self._anime_id = anime_id
        self._is_loaded = False

        self.__anime_url = self.ANIME_URL.format(self._anime_id)

        ### Getting staff from html
        ## staff from side content
        self.__title = ''
        self.__image_url = ''
        self.__english = ''
        self.__synonyms = ''
        self.__japanese = ''
        self.__type = ''
        self.__episodes = 0
        self.__status = ''
        self.__aired = ''
        self.__producers = dict()
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

    @property
    def id(self):
        return self._anime_id

    @property
    @load
    def title(self):
        return self.__title

    @property
    @load
    def image_url(self):
        return self.__image_url

    @property
    @load
    def english(self):
        return self.__english

    @property
    @load
    def synonyms(self):
        return self.__synonyms

    @property
    @load
    def japanese(self):
        return self.__japanese

    @property
    @load
    def type(self):
        return self.__type

    @property
    @load
    def episodes(self):
        return self.__episodes

    @property
    @load
    def status(self):
        return self.__status

    @property
    @load
    def aired(self):
        return self.__aired

    @property
    @load
    def producers(self):
        return self.__producers

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

    def reload(self):
        # Getting content wrapper <div>
        content_wrapper_div = self._get_content_wrapper_div(self.__anime_url, connect)

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

        # episodes <div>
        episodes_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Episodes', episodes_div)
        episodes_span, self_episodes = episodes_div.contents
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
        aired_span, self.__aired = aired_div.contents
        self.__aired = self.__aired.strip()
        # TODO: split __aired to more data
        side_contents_divs_index += 1

        # producers <div>
        producers_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Producers', producers_div)
        for producer_link in producers_div.findAll(name='a'):
            self.__producers[producer_link.text] = producer_link['href']
        side_contents_divs_index += 1

        # genres <div>
        genres_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Genres', genres_div)
        for genre_link in genres_div.findAll(name='a'):
            self.__genres[genre_link.text] = genre_link['href']
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
            assert 6 == len(synopsis_cell_contents), \
                "Got len(synopsis_cell_contents) == {0:d}".format(len(synopsis_cell_contents))
        len(synopsis_cell.contents)
        if DEBUG:
            assert 'Synopsis' == synopsis_cell.h2.text
        self.__synopsis = synopsis_cell_contents[1]

        # Getting other data
        main_content_other_data = main_content_other_data.td
        other_data_kids = [i for i in main_content_other_data.children]

        # Getting all the data under 'Related Anime'
        related_str_to_list_dict = {
            'Adaptation:': self.__adaptations,
            'Character:': self.__characters,
            'Sequel:': self.__sequals,
            'Prequel:': self.__prequel,
            'Spin-off:': self.__spin_offs,
            'Alternative version:': self.__alternative_versions,
            'Side story:': self.__side_story,
        }

        index = 0
        index = get_next_index(index, other_data_kids)
        assert 'h2' == other_data_kids[index].name
        assert 'Related Anime' == other_data_kids[index].text

        index += 1
        while other_data_kids[index + 1].name != 'br':
            index = make_list(related_str_to_list_dict[other_data_kids[index].strip()], index, other_data_kids)
        next_index = get_next_index(index, other_data_kids)

        if DEBUG:
            assert next_index - index == 2
            index = next_index + 1

            # Getting all the data under 'Characters & Voice Actors'
            assert 'h2' == other_data_kids[index].name
            assert 'Characters & Voice Actors' == other_data_kids[index].contents[-1]

        self._is_loaded = True

    def __eq__(self, other):
        if not issubclass(Anime, other):
            return False
        return self._anime_id == other._anime_id

    def __repr__(self):
        return "<{0:s}  id={1:d}>".format(self.__class__.__name__, self._anime_id)