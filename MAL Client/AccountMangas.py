from xml.etree import ElementTree
from threading import Thread
from consts import HOST_NAME, DEBUG
from decorators import load
from MyManga import MyManga
from urllib import request


class AccountMangas(object):
        URL = request.urljoin(HOST_NAME, "malappinfo.php?u={0:s}&type=manga")

        def __init__(self, username: str, connection):
            self.__connection = connection
            self.__url = self.URL.format(username)

            self.__reading = []
            self.__completed = []
            self.__on_hold = []
            self.__dropped = []
            self.__plan_to_read = []

            self.map_of_lists = {
                1: self.__reading,
                2: self.__completed,
                3: self.__on_hold,
                4: self.__dropped,
                6: self.__plan_to_read,

                '1': self.__reading,
                '2': self.__completed,
                '3': self.__on_hold,
                '4': self.__dropped,
                '6': self.__plan_to_read,

                'reading': self.__reading,
                'completed': self.__completed,
                'onhold': self.__on_hold,
                'dropped': self.__dropped,
                'plantoread': self.__plan_to_read,
            }

            self._is_loaded = False

        @property
        @load
        def reading(self) -> list:
            return self.__reading

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
        def plan_to_read(self) -> list:
            return self.__plan_to_read

        def __contains__(self, item: str or int) -> bool:
            item = str(item)
            if item.isdigit():
                return int(item) in MyManga.STATUS_MAP_FROM_STRING_TO_NUMBER.values()
            return item in MyManga.STATUS_MAP_FROM_STRING_TO_NUMBER.keys()

        def __iter__(self):
            class AccountMangasIterator(object):
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
            return AccountMangasIterator(self.reading + self.completed + self.on_hold + self.dropped + self.plan_to_read)

        def __getitem__(self, key: str or int) -> list:
            if type(key) == int:
                if key < len(self.reading):
                    return self.reading[key]
                key -= len(self.reading)
                if key < len(self.completed):
                    return self.completed[key]
                key -= len(self.completed)
                if key < len(self.on_hold):
                    return self.on_hold[key]
                key -= len(self.on_hold)
                if key < len(self.dropped):
                    return self.dropped[key]
                key -= len(self.dropped)
                if key < len(self.plan_to_read):
                    return self.plan_to_read[key]
                raise IndexError('list index out of range (the size if {0:d}'.format(len(self)))
            key = str(key)
            for manga in self:
                if manga.title == key:
                    return manga
            KeyError("{0:s} doesn't have the anime '{1:s}'".format(self.__class__.__name__, key))

        def reload(self):
            resp_data = self.__connection.auth_connect(self.__url)
            xml_tree = ElementTree.fromstring(resp_data)
            assert 'myanimelist' == xml_tree.tag, 'myanimelist == {0:s}'.format(xml_tree.tag)
            xml_mangas = xml_tree.getchildren()
            xml_general_data = xml_mangas[0]
            assert 'myinfo' == xml_general_data.tag, 'myinfo == {0:s}'.format(xml_general_data.tag)
            l = xml_general_data.getchildren()
            xml_user_id = l[0]
            assert 'user_id' == xml_user_id.tag, 'user_id == {0:s}'.format(xml_user_id.tag)
            assert self.__connection.is_user_by_id(int(xml_user_id.text.strip())), int(xml_user_id.text.strip())
            xml_user_name = l[1]
            assert 'user_name' == xml_user_name.tag, 'user_name == {0:s}'.format(xml_user_name.tag)
            assert self.__connection.is_user_by_name(xml_user_name.text.strip()), xml_user_name.text.strip()
            xml_user_reading = l[2]
            assert 'user_reading' == xml_user_reading.tag, 'user_reading == {0:s}'.format(xml_user_reading.tag)
            xml_user_completed = l[3]
            assert 'user_completed' == xml_user_completed.tag, 'user_completed == {0:s}'.format(xml_user_completed.tag)
            xml_user_onhold = l[4]
            assert 'user_onhold' == xml_user_onhold.tag, 'user_onhold == {0:s}'.format(xml_user_onhold.tag)
            xml_user_dropped = l[5]
            assert 'user_dropped' == xml_user_dropped.tag, 'user_dropped == {0:s}'.format(xml_user_dropped.tag)
            xml_user_plantoread = l[6]
            assert 'user_plantoread' == xml_user_plantoread.tag, 'user_plantoread == {0:s}'.format(xml_user_plantoread.tag)
            xml_user_days_spent_watching = l[7]
            assert 'user_days_spent_watching' == xml_user_days_spent_watching.tag, 'user_days_spent_watching == {0:s}'.format(xml_user_days_spent_watching.tag)
            self.user_days_spent_watching = float(xml_user_days_spent_watching.text.strip())

            xml_mangas = xml_mangas[1:]

            self.__reading.clear()
            self.__completed.clear()
            self.__on_hold.clear()
            self.__dropped.clear()
            self.__plan_to_read.clear()

            threads = []
            print(len(xml_mangas))
            for xml_manga in xml_mangas:
                if DEBUG:
                    self._get_manga(xml_manga)
                else:
                    thread = Thread(target=self._get_manga, args=(xml_manga, ))
                    thread.start()
                    threads.append(thread)

            while threads:
                threads.pop().join()

            if len(self.__reading) != int(xml_user_reading.text.strip()):
                print("reading: {0:d} != {1:d}".format(len(self.__reading), int(xml_user_reading.text.strip())))
            if len(self.__completed) != int(xml_user_completed.text.strip()):
                print("completed: {0:d} != {1:d}".format(len(self.__completed), int(xml_user_completed.text.strip())))
            if len(self.__on_hold) != int(xml_user_onhold.text.strip()):
                print("on hold: {0:d} != {1:d}".format(len(self.__on_hold), int(xml_user_onhold.text.strip())))
            if len(self.__dropped) != int(xml_user_dropped.text.strip()):
                print("dropped: {0:d} != {1:d}".format(len(self.__dropped), int(xml_user_dropped.text.strip())))
            if len(self.__plan_to_read) != int(xml_user_plantoread.text.strip()):
                print("plan to read: {0:d} != {1:d}".format(len(self.__plan_to_read), int(xml_user_plantoread.text.strip())))
            """
            assert len(self.__reading) == int(xml_user_reading.text.strip()),\
                "reading: {0:d} != {1:d}".format(len(self.__reading), int(xml_user_reading.text.strip()))
            assert len(self.__completed) == int(xml_user_completed.text.strip()),\
                "completed: {0:d} != {1:d}".format(len(self.__completed), int(xml_user_completed.text.strip()))
            assert len(self.__on_hold) == int(xml_user_onhold.text.strip()),\
                "on hold: {0:d} != {1:d}".format(len(self.__on_hold), int(xml_user_onhold.text.strip()))
            assert len(self.__dropped) == int(xml_user_dropped.text.strip()),\
                "dropped: {0:d} != {1:d}".format(len(self.__dropped), int(xml_user_dropped.text.strip()))
            assert len(self.__plan_to_read) == int(xml_user_plantoread.text.strip()),\
                "plan to read: {0:d} != {1:d}".format(len(self.__plan_to_read), int(xml_user_plantoread.text.strip()))
            """
            self._is_loaded = True

        def _get_manga(self, xml_manga: ElementTree.Element):
            manga_id_xml = xml_manga.find('series_mangadb_id')
            assert manga_id_xml is not None
            try:
                manga = MyManga(int(manga_id_xml.text.strip()), self.__connection, my_xml=xml_manga)
            except AssertionError as err:
                print('AssertionError', err)
                return
            try:
                self.map_of_lists[manga.my_status].append(manga)
                #print("Added", manga, "to ", manga.my_status)
            except KeyError as err:
                print("Got an key error:", err)

        def __len__(self):
            return len(self.reading) + len(self.completed) + len(self.on_hold) + len(self.dropped) +\
                   len(self.plan_to_read)

        def __repr__(self):
            return "<User mangas' number is {0:d}>".format(len(self))