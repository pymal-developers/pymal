import bs4
from pymal.consts import RETRY_NUMBER, RETRY_SLEEP
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

    def __init__(self):
        self._id = 0
        self._is_loaded = False

        self.__malurl = ''

        ### Getting staff from html
        ## staff from side content
        self.__title = None
        self.__image_url = None
        self.__english = ''
        self.__synonyms = None
        self.__japanese = ''
        self.__type = None
        self.__status = None
        self.__start_time = None
        self.__end_time = None
        self.__creators = dict()
        self.__genres = dict()
        self.__rating = 0
        self.__score = 0.0
        self.__rank = 0
        self.__popularity = 0

        ## staff from main content
        #staff from row 1
        self.__synopsis = ''

        #staff from row 2
        self.__adaptations = set()
        self.__characters = set()
        self.__sequals = set()
        self.__prequel = set()
        self.__spin_offs = set()
        self.__alternative_versions = set()
        self.__side_story = set()
        self.__summary = set()
        self.__other = set()
        self.__parent_story = set()
        self.__alternative_setting = set()

        self.related_str_to_list_dict = {
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

    @property
    def id(self):
        return self._id

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
    def creators(self):
        return self.__creators

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
        raise NotImplemented

    def __repr__(self):
        return "<{0:s} id={1:d}>".format(self.__class__.__name__, self._id)

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
