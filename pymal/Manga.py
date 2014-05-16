from urllib import request
from pymal.consts import HOST_NAME, DEBUG, SITE_PUBLISHED_FORMAT_TIME, MALAPPINFO_FORMAT_TIME, XMLS_DIRECTORY
from pymal.decorators import load
from pymal.MALObject import MALObject, check_side_content_div
from pymal.global_functions import connect, make_list, get_next_index
import time
from os import path


class Manga(MALObject):
    GLOBAL_MAL_URL = request.urljoin(HOST_NAME, "manga/{0:d}")
    MY_MAL_XML_TEMPLATE_PATH = path.join(path.dirname(__file__), XMLS_DIRECTORY, 'myanimelist_official_api_manga.xml')
    MY_MAL_ADD_URL = request.urljoin(HOST_NAME, 'api/mangalist/add/{0:d}.xml')

    def __init__(self, manga_id: int, manga_xml=None):
        super().__init__()

        self._id = manga_id
        self._is_loaded = False

        self._mal_url = self.GLOBAL_MAL_URL.format(self._id)

        ### Getting staff from html
        ## staff from side content
        self._chapters = None
        self._volumes = None

        if manga_xml is not None:
            self._title = manga_xml.find('series_title').text.strip()
            self._synonyms = manga_xml.find('series_synonyms').text
            if self._synonyms is not None:
                self._synonyms = self._synonyms.strip()
            # TODO: make this number to a string (or the string to a number?)
            self._type = manga_xml.find('series_type').text.strip()
            self._chapters = int(manga_xml.find('series_chapters').text.strip())
            self._volumes = int(manga_xml.find('series_volumes').text.strip())
            try:
                self._status = int(manga_xml.find('series_status').text.strip())
            except ValueError:
                self._status = manga_xml.find('series_status').text.strip()
                print('self._status=', self._status)
            start_time = manga_xml.find('series_start').text.strip()
            if start_time == '0000-00-00':
                self._start_time = float('inf')
            else:
                start_time = start_time[:4] + start_time[4:].replace('00', '01')
                self._start_time = time.mktime(time.strptime(start_time, MALAPPINFO_FORMAT_TIME))
            end_time = manga_xml.find('series_end').text.strip()
            if end_time == '0000-00-00':
                self._end_time = float('inf')
            else:
                end_time = end_time[:4] + end_time[4:].replace('00', '01')
                self._end_time = time.mktime(time.strptime(end_time, MALAPPINFO_FORMAT_TIME))
            self._image_url = manga_xml.find('series_image').text.strip()

    @property
    def volumes(self):
        if self._volumes is None:
            self.reload()
        return self._volumes

    @property
    def chapters(self):
        if self._chapters is None:
            self.reload()
        return self._chapters

    def reload(self):
        # Getting content wrapper <div>
        content_wrapper_div = self._get_content_wrapper_div(self._mal_url, connect)

        # Getting title <div>
        self._title = content_wrapper_div.h1.contents[1].strip()

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
        self._image_url = img_link.img['src']

        side_contents_divs_index = 3
        # english <div>
        english_div = side_contents_divs[side_contents_divs_index]
        if check_side_content_div('English', english_div):
            english_span, self._english = english_div.contents
            self._english = self._english.strip()
            side_contents_divs_index += 1
        else:
            self._english = ''

        # synonyms <div>
        synonyms_div = side_contents_divs[side_contents_divs_index]
        if check_side_content_div('Synonyms', synonyms_div):
            synonyms_span, self._synonyms = synonyms_div.contents
            self._synonyms = self._synonyms.strip()
            side_contents_divs_index += 1
        else:
            self._synonyms = ''

        # japanese <div>
        japanese_div = side_contents_divs[side_contents_divs_index]
        if check_side_content_div('Japanese', japanese_div):
            japanese_span, self._japanese = japanese_div.contents
            self._japanese = self._japanese.strip()
            side_contents_divs_index += 1
        else:
            self._japanese = ''

        # type <div>
        type_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Type', type_div)
        type_span, self._type = type_div.contents
        self._type = self._type.strip()
        side_contents_divs_index += 1

        # volumes <div>
        volumes_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Volumes', volumes_div)
        volumes_span, self_volumes = volumes_div.contents
        self_volumes = self_volumes.strip()
        if self_volumes.isdigit():
            self._volumes = int(self_volumes)
        else:
            assert 'Unknown' == self_volumes, "Unknown == '{0:s}'".format(self_volumes)
            self._volumes = float('inf')

        side_contents_divs_index += 1

        # chapters <div>
        chapters_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Chapters', chapters_div)
        chapters_span, self_chapters = chapters_div.contents
        self_chapters = self_chapters .strip()
        if self_chapters.isdigit():
            self._chapters = int(self_chapters)
        else:
            assert 'Unknown' == self_chapters, "Unknown == '{0:s}'".format(self_chapters)
            self._chapters = float('inf')
        side_contents_divs_index += 1

        # status <div>
        status_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Status', status_div)
        status_span, self._status = status_div.contents
        self._status = self._status.strip()
        side_contents_divs_index += 1

        # published <div>
        published_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Published', published_div)
        published_span, published = published_div.contents
        start_time, end_time = published.split('to')
        start_time, end_time = start_time.strip(), end_time.strip()
        if '?' == start_time:
            self._start_time = float('inf')
        else:
            self._start_time = time.mktime(time.strptime(start_time, SITE_PUBLISHED_FORMAT_TIME))
        if '?' == end_time:
            self._end_time = float('inf')
        else:
            self._end_time = time.mktime(time.strptime(end_time, SITE_PUBLISHED_FORMAT_TIME))
        side_contents_divs_index += 1

        # genres <div>
        genres_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Genres', genres_div)
        for genre_link in genres_div.findAll(name='a'):
            self._genres[genre_link.text.strip()] = genre_link['href']
        side_contents_divs_index += 1

        # authors <div>
        authors_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Authors', authors_div)
        for authors_link in authors_div.findAll(name='a'):
            self._creators[authors_link.text.strip()] = authors_link['href']
        side_contents_divs_index += 1

        side_contents_divs_index += 1

        # score <div>
        score_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Score', score_div)
        score_span, self_score = score_div.contents[:2]
        self._score = float(self_score.strip())
        side_contents_divs_index += 1

        # rank <div>
        rank_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Ranked', rank_div)
        rank_span, self_rank = rank_div.contents[:2]
        self_rank = self_rank.strip()
        assert self_rank.startswith("#")
        self._rank = int(self_rank[1:])
        side_contents_divs_index += 1

        # popularity <div>
        popularity_div = side_contents_divs[side_contents_divs_index]
        assert check_side_content_div('Popularity', popularity_div)
        popularity_span, self_popularity = popularity_div.contents[:2]
        self_popularity = self_popularity.strip()
        assert self_popularity.startswith("#")
        self._popularity = int(self_popularity[1:])

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
        self._synopsis = synopsis_cell_contents[1]

        # Getting other data
        main_content_other_data = main_content_other_data.td
        other_data_kids = [i for i in main_content_other_data.children]

        # Getting all the data under 'Related Manga'
        index = 0
        index = get_next_index(index, other_data_kids)
        if 'h2' == other_data_kids[index].name and 'Related Manga' == other_data_kids[index].text.strip():
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
            assert 'h2' == other_data_kids[index].name, 'h2 == {0:s}'.format(other_data_kids[index].name)
            assert 'Characters' == other_data_kids[index].contents[-1], 'Characters == {0:s}'.format(other_data_kids[index].contents[-1])

        self._is_loaded = True

    def add(self):
        data = self.MY_MAL_XML_TEMPLATE.format(0, 0, 6, 0, 0, 0, 0, '00000000', '00000000', 0, False, False, '', '', '', 0)
        print(connect(self.MY_MAL_ADD_URL.format()))

    def __eq__(self, other):
        if not issubclass(Manga, other):
            return False
        return self._id == other._id
