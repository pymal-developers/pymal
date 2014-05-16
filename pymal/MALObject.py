import bs4
from pymal.consts import RETRY_NUMBER, RETRY_SLEEP, MALAPPINFO_FORMAT_TIME
from pymal.decorators import load
import time


def check_side_content_div(expected_text: str, div_node: bs4.element.Tag):
    span_node = div_node.span
    assert span_node is not None, div_node
    expected_text += ":"
    return ['dark_text'] == span_node['class'] and expected_text == span_node.text.strip()


class MALObject(object):
    def _get_myanimelist_div(self, url: str, connection_function) -> bs4.element.Tag:
        got_robot = False
        for try_number in range(RETRY_NUMBER):
            time.sleep(RETRY_SLEEP)
            data = connection_function(url)
            html = bs4.BeautifulSoup(data, "html5lib").html
            if html.head.find(name="meta", attrs={"name": "robots"}) is not None:
                got_robot = True
                continue
            div = html.body.find(name="div", attrs={"id": 'myanimelist'})
            if div is not None:
                return div
        assert not got_robot, "Got robot."
        assert False, "my anime list div wasnt found"

    def _get_content_wrapper_div(self, url: str, connection_function) -> bs4.element.Tag:
        myanimelist_div = self._get_myanimelist_div(url, connection_function)

        # Getting content wrapper <div>
        content_wrapper_div = myanimelist_div.find(name="div", attrs={"id": "contentWrapper"}, recursive=False)
        assert content_wrapper_div is not None
        return content_wrapper_div

    GLOBAL_MAL_URL = None
    MY_MAL_XML_TEMPLATE_PATH = None
    MY_MAL_ADD_URL = None

    def __init__(self, mal_xml=None):
        self._id = 0
        self._is_loaded = False

        self._mal_url = ''

        ### Getting staff from html
        ## staff from side content
        self._title = None
        self._image_url = None
        self._english = ''
        self._synonyms = None
        self._japanese = ''
        self._type = None
        self._status = None
        self._start_time = None
        self._end_time = None
        self._creators = dict()
        self._genres = dict()
        self._score = 0.0
        self._rank = 0
        self._popularity = 0

        ## staff from main content
        #staff from row 1
        self._synopsis = ''

        #staff from row 2
        self._adaptations = list()
        self._characters = list()
        self._sequals = list()
        self._prequel = list()
        self._spin_offs = list()
        self._alternative_versions = list()
        self._side_stories = list()
        self._summaries = list()
        self._others = list()
        self._parent_stories = list()
        self._alternative_settings = list()

        self.related_str_to_list_dict = {
            'Adaptation:': self._adaptations,
            'Character:': self._characters,
            'Sequel:': self._sequals,
            'Prequel:': self._prequel,
            'Spin-off:': self._spin_offs,
            'Alternative version:': self._alternative_versions,
            'Side story:': self._side_stories,
            'Summary:': self._summaries,
            'Other:': self._others,
            'Parent story:': self._parent_stories,
            'Alternative setting:': self._alternative_settings,
        }

        if mal_xml is not None:
            self._title = mal_xml.find('series_title').text.strip()
            self._synonyms = mal_xml.find('series_synonyms').text
            if self._synonyms is not None:
                self._synonyms = self._synonyms.strip()
            # TODO: make this number to a string (or the string to a number?)
            self._type = mal_xml.find('series_type').text.strip()
            try:
                self._status = int(mal_xml.find('series_status').text.strip())
            except ValueError:
                self._status = mal_xml.find('series_status').text.strip()
                print('self._status=', self._status)
            start_time = mal_xml.find('series_start').text.strip()
            if start_time == '0000-00-00':
                self._start_time = float('inf')
            else:
                start_time = start_time[:4] + start_time[4:].replace('00', '01')
                self._start_time = time.mktime(time.strptime(start_time, MALAPPINFO_FORMAT_TIME))
            end_time = mal_xml.find('series_end').text.strip()
            if end_time == '0000-00-00':
                self._end_time = float('inf')
            else:
                end_time = end_time[:4] + end_time[4:].replace('00', '01')
                self._end_time = time.mktime(time.strptime(end_time, MALAPPINFO_FORMAT_TIME))
            self._image_url = mal_xml.find('series_image').text.strip()

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        if self._title is None:
            self.reload()
        return self._title

    @property
    def image_url(self):
        if self._image_url is None:
            self.reload()
        return self._image_url

    @property
    @load
    def english(self):
        return self._english

    @property
    def synonyms(self):
        if self._synonyms is None:
            self.reload()
        return self._synonyms

    @property
    @load
    def japanese(self):
        return self._japanese

    @property
    def type(self):
        if self._type is None:
            self.reload()
        return self._type

    @property
    def status(self):
        if self._status is None:
            self.reload()
        return self._status

    @property
    def start_time(self):
        if self._start_time is None:
            self.reload()
        return self._start_time

    @property
    def end_time(self):
        if self._end_time is None:
            self.reload()
        return self._end_time

    @property
    @load
    def creators(self):
        return self._creators

    @property
    @load
    def genres(self):
        return self._genres

    @property
    @load
    def score(self):
        return self._score

    @property
    @load
    def rank(self):
        return self._rank

    @property
    @load
    def popularity(self):
        return self._popularity

    @property
    @load
    def synopsis(self):
        return self._synopsis

    # staff from main content
    @property
    @load
    def adaptations(self):
        return self._adaptations

    @property
    @load
    def characters(self):
        return self._characters

    @property
    @load
    def sequals(self):
        return self._sequals

    @property
    @load
    def prequel(self):
        return self._prequel

    @property
    @load
    def spin_offs(self):
        return self._spin_offs

    @property
    @load
    def alternative_versions(self):
        return self._alternative_versions

    @property
    @load
    def side_stories(self):
        return self._side_stories

    @property
    @load
    def summaries(self):
        return self._summaries

    @property
    @load
    def others(self):
        return self._others

    @property
    @load
    def parent_stories(self):
        return self._parent_stories

    @property
    @load
    def alternative_settings(self):
        return self._alternative_settings

    def reload(self):
        raise NotImplemented

    def __repr__(self):
        try:
            title = ' ' + self.title
        except:
            title = ''
        return "<{0:s}{1:s} id={2:d}>".format(self.__class__.__name__, title, self._id)

    @property
    def to_xml(self):
        raise NotImplemented

    @property
    def MY_MAL_XML_TEMPLATE(self):
        with open(self.MY_MAL_XML_TEMPLATE_PATH) as f:
            data = f.read()
        return data

    def add(self):
        raise NotImplemented
