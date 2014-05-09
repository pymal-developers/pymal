from xml.etree import ElementTree
from threading import Thread
from pymal.consts import HOST_NAME, DEBUG
from pymal.decorators import load
from pymal.MyAnime import MyAnime
from urllib import request


class AccountAnimes(object):
    URL = request.urljoin(HOST_NAME, "malappinfo.php?u={0:s}&type=anime")

    def __init__(self, username: str, connection):
        self.__connection = connection
        self.__url = self.URL.format(username)

        self.__watching = []
        self.__completed = []
        self.__on_hold = []
        self.__dropped = []
        self.__plan_to_watch = []

        self.map_of_lists = {
            1: self.__watching,
            2: self.__completed,
            3: self.__on_hold,
            4: self.__dropped,
            6: self.__plan_to_watch,

            '1': self.__watching,
            '2': self.__completed,
            '3': self.__on_hold,
            '4': self.__dropped,
            '6': self.__plan_to_watch,

            'watching': self.__watching,
            'completed': self.__completed,
            'onhold': self.__on_hold,
            'dropped': self.__dropped,
            'plantowatch': self.__plan_to_watch,
        }

        self._is_loaded = False

    @property
    @load
    def watching(self) -> list:
        return self.__watching

    @property
    @load
    def completed(self) -> list:
        return self.__completed

    @property
    @load
    def on_hold(self) -> list:
        return self.__on_hold

    @property
    @load
    def dropped(self) -> list:
        return self.__dropped

    @property
    @load
    def plan_to_watch(self) -> list:
        return self.__plan_to_watch

    def __contains__(self, item: MyAnime) -> bool:
        return item in self.watching or item in self.completed or item in self.on_hold or item in self.dropped or item in self.plan_to_watch

    def __iter__(self):
        class AccountAnimesIterator(object):
            def __init__(self, values):
                self. values = values
                self.location = 0

            def __iter__(self):
                self.location = 0
                return self

            def __next__(self):
                if self.location >= len(self.values):
                    raise StopIteration
                value = self.values[self.location]
                self.location += 1
                return value
        return AccountAnimesIterator(self.watching + self.completed + self.on_hold + self.dropped + self.plan_to_watch)

    def __getitem__(self, key: str or int) -> list:
        if type(key) == int:
            if key < len(self.watching):
                return self.watching[key]
            key -= len(self.watching)
            if key < len(self.completed):
                return self.completed[key]
            key -= len(self.completed)
            if key < len(self.on_hold):
                return self.on_hold[key]
            key -= len(self.on_hold)
            if key < len(self.dropped):
                return self.dropped[key]
            key -= len(self.dropped)
            if key < len(self.plan_to_watch):
                return self.plan_to_watch[key]
            raise IndexError('list index out of range (the size if {0:d}'.format(len(self)))
        key = str(key)
        for anime in self:
            if anime.title == key:
                return anime
        KeyError("{0:s} doesn't have the anime '{1:s}'".format(self.__class__.__name__, key))

    def reload(self):
        resp_data = self.__connection.auth_connect(self.__url)
        xml_tree = ElementTree.fromstring(resp_data)
        assert 'myanimelist' == xml_tree.tag, 'myanimelist == {0:s}'.format(xml_tree.tag)
        xml_animes = xml_tree.getchildren()
        xml_general_data = xml_animes[0]
        assert 'myinfo' == xml_general_data.tag, 'myinfo == {0:s}'.format(xml_general_data.tag)
        l = xml_general_data.getchildren()
        xml_user_id = l[0]
        assert 'user_id' == xml_user_id.tag, 'user_id == {0:s}'.format(xml_user_id.tag)
        assert self.__connection.is_user_by_id(int(xml_user_id.text.strip())), int(xml_user_id.text.strip())
        xml_user_name = l[1]
        assert 'user_name' == xml_user_name.tag, 'user_name == {0:s}'.format(xml_user_name.tag)
        assert self.__connection.is_user_by_name(xml_user_name.text.strip()), xml_user_name.text.strip()
        xml_user_watching = l[2]
        assert 'user_watching' == xml_user_watching.tag, 'user_watching == {0:s}'.format(xml_user_watching.tag)
        xml_user_completed = l[3]
        assert 'user_completed' == xml_user_completed.tag, 'user_completed == {0:s}'.format(xml_user_completed.tag)
        xml_user_onhold = l[4]
        assert 'user_onhold' == xml_user_onhold.tag, 'user_onhold == {0:s}'.format(xml_user_onhold.tag)
        xml_user_dropped = l[5]
        assert 'user_dropped' == xml_user_dropped.tag, 'user_dropped == {0:s}'.format(xml_user_dropped.tag)
        xml_user_plantowatch = l[6]
        assert 'user_plantowatch' == xml_user_plantowatch.tag, 'user_plantowatch == {0:s}'.format(xml_user_plantowatch.tag)

        xml_animes = xml_animes[1:]

        self.__watching.clear()
        self.__completed.clear()
        self.__on_hold.clear()
        self.__dropped.clear()
        self.__plan_to_watch.clear()

        threads = []
        for xml_anime in xml_animes:
            pass
            if DEBUG:
                self.__get_anime(xml_anime)
            else:
                thread = Thread(target=self.__get_anime, args=(xml_anime, ))
                thread.start()
                threads.append(thread)

        while threads:
            threads.pop().join()

        if len(self.__watching) != int(xml_user_watching.text.strip()):
            print('watching: {0:d} != {1:d}'.format(len(self.__watching), int(xml_user_watching.text.strip())))
        if len(self.__completed) != int(xml_user_completed.text.strip()):
            print('completed: {0:d} != {1:d}'.format(len(self.__completed), int(xml_user_completed.text.strip())))
        if len(self.__on_hold) != int(xml_user_onhold.text.strip()):
            print('on hold:{0:d} != {1:d}'.format(len(self.__on_hold), int(xml_user_onhold.text.strip())))
        if len(self.__dropped) != int(xml_user_dropped.text.strip()):
            print('dropped: {0:d} != {1:d}'.format(len(self.__dropped), int(xml_user_dropped.text.strip())))
        if len(self.__plan_to_watch) != int(xml_user_plantowatch.text.strip()):
            print('plan to watch: {0:d} != {1:d}'.format(len(self.__plan_to_watch), int(xml_user_plantowatch.text.strip())))
        """
        assert len(self.__watching) == int(xml_user_watching.text.strip()),\
            '{0:d} == {1:d}'.format(len(self.__watching), int(xml_user_watching.text.strip()))
        assert len(self.__completed) == int(xml_user_completed.text.strip()),\
            '{0:d} == {1:d}'.format(len(self.__completed), int(xml_user_completed.text.strip()))
        assert len(self.__on_hold) == int(xml_user_onhold.text.strip()),\
            '{0:d} == {1:d}'.format(len(self.__on_hold), int(xml_user_onhold.text.strip()))
        assert len(self.__dropped) == int(xml_user_dropped.text.strip()),\
            '{0:d} == {1:d}'.format(len(self.__dropped), int(xml_user_dropped.text.strip()))
        assert len(self.__plan_to_watch) == int(xml_user_plantowatch.text.strip()),\
            '{0:d} == {1:d}'.format(len(self.__plan_to_watch), int(xml_user_plantowatch.text.strip()))
        """
        self._is_loaded = True

    def __get_anime(self, anime_xml: ElementTree.Element):
        anime_id_xml = anime_xml.find('series_animedb_id')
        assert anime_id_xml is not None
        try:
            anime = MyAnime(int(anime_id_xml.text.strip()), self.__connection, my_xml=anime_xml)
        except AssertionError as err:
            print('AssertionError', err)
            return
        try:
            self.map_of_lists[anime.my_status].append(anime)
            #print("Added", anime, "to ", anime.my_status)
        except KeyError as err:
            print("Got an key error:", err)

    def __len__(self):
        return len(self.watching) + len(self.completed) + len(self.on_hold) + len(self.dropped) +\
               len(self.plan_to_watch)

    def __repr__(self):
        return "<User animes' number is {0:d}>".format(len(self))