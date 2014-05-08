from xml.etree import ElementTree
from threading import Thread
import consts
from decorators import load
from MyAnime import MyAnime
from Anime import Anime


class AccountAnimes(object):
    URL = r"http://myanimelist.net/malappinfo.php?u={0:s}&type=anime"

    def __init__(self, username: str, connection):
        self.__connection = connection
        self.__url = self.URL.format(username)

        self.__watching = []
        self.__completed = []
        self.__on_hold = []
        self.__dropped = []
        self.__plan_to_watch = []

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
        if self.__dropped is None:
            self.refresh()
        return self.__dropped

    @property
    @load
    def plan_to_watch(self) -> list:
        return self.__plan_to_watch

    def __contains__(self, item: Anime) -> bool:
        return item in self.watching or item in self.completed or item in self.on_hold or item in self.dropped or item in self.plan_to_watch

    def __getitem__(self, key: str or int) -> list:
        key = str(key)
        e = 'AccountanimeData gets only the keys: 1, 2, 3, 4, 6, watching, completed, onhold, dropped, plantowatch'
        if '1' == key or 'watching' == key:
            return self.watching
        elif '2' == key or 'completed' == key:
            return self.completed
        elif '3' == key or 'onhold' == key:
            return self.on_hold
        elif '4' == key or 'dropped' == key:
            return self.dropped
        elif '6' == key or 'plantowatch' == key:
            return self.plan_to_watch
        else:
            raise KeyError(e)

    def refresh(self):
        resp_data = self.__connection.connect(self.__url)
        xml_tree = ElementTree.fromstring(resp_data)
        assert 'myanimelist' == xml_tree.tag
        xml_animes = xml_tree.getchildren()
        xml_general_data = xml_animes[0]
        assert 'myinfo' == xml_general_data.tag
        l = xml_general_data.getchildren()
        xml_user_id = l[0]
        assert 'user_id' == xml_user_id.tag
        xml_user_name = l[1]
        assert 'user_name' == xml_user_name.tag
        assert self.__connection.is_user(xml_user_name.text, int(xml_user_id.text))
        xml_user_watching = l[2]
        assert 'user_watching' == xml_user_watching.tag
        xml_user_completed = l[3]
        assert 'user_completed' == xml_user_completed.tag
        xml_user_onhold = l[4]
        assert 'user_onhold' == xml_user_onhold.tag
        xml_user_dropped = l[5]
        assert 'user_dropped' == xml_user_dropped.tag
        xml_user_plantowatch = l[6]
        assert 'user_plantowatch' == xml_user_plantowatch.tag

        xml_animes = xml_animes[1:]

        self.__watching.clear()
        self.__completed.clear()
        self.__on_hold.clear()
        self.__dropped.clear()
        self.__plan_to_watch.clear()

        threads = []
        for xml_anime in xml_animes:
            pass
            if consts.DEBUG:
                self.get_anime(xml_anime)
            else:
                thread = Thread(target=self.get_anime, args=(xml_anime, ))
                thread.start()
                threads.append(thread)

        while threads:
            threads.pop().join()

        if consts.DEBUG:
            assert self.__watching == int(xml_user_watching.text)
            assert self.__completed == int(xml_user_completed.text)
            assert self.__on_hold == int(xml_user_onhold.text)
            assert self.__dropped == int(xml_user_dropped.text)
            assert self.__plan_to_watch == int(xml_user_plantowatch.text)

    def get_anime(self, anime_id: int):
        import pdb
        pdb.set_trace()
        anime = MyAnime(anime_id, self.__connection)
        try:
            self[anime.my_status].append(anime)
        except Exception as e:
            print(e)

    @load
    def __len__(self):
        return len(self.__watching) + len(self.__completed) + len(self.__on_hold) + len(self.__dropped) + len(self.plan_to_watch)

    def __repr__(self):
        return "<User animes' number is {0:d}>".format(len(self))