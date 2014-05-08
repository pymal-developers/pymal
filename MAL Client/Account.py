import base64
from xml.etree import ElementTree
from urllib.error import HTTPError
import time
from global_functions import _connect
from decorators import load
import consts
from AccountAnimes import AccountAnimes


class Account(object):
    AUTH_CHECKER_URL = r'http://myanimelist.net/api/account/verify_credentials.xml'

    def __init__(self, username: str, password: str or None=None):
        self._username = username
        self._password = password
        self.__user_id = 0
        self.__auth_string = ''
        self.__cookies = dict()

        self.__is_loaded = False
        self.__animes = None
        self.__mangas = None

        if password is not None:
            self.change_password(password)

    @load
    @property
    def animes(self):
        return self.__animes

    def reload(self):
        self.__animes = AccountAnimes(self._username, self)
        self.__is_loaded = True

    def change_password(self, password: str) -> bool:
        """Checking if the new password is valid"""
        auth_string = '{0:s}:{1:s}'.format(self._username, password)
        auth_string = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8').replace('\n', '')
        self.__auth_string = 'Basic %s' % auth_string

        tries = 0
        try_again = True
        while try_again:
            tries += 1
            try:
                data = self.auth_connect(self.AUTH_CHECKER_URL)
            except HTTPError as e:
                self.__auth_string = ''
                if e.code == 401:
                    return False
                raise
            try:
                xml_user = ElementTree.fromstring(data)
            except ElementTree.ParseError as e:
                if e.code != 4:
                    raise
                elif tries > consts.RETRY_NUMBER:
                    raise
                time.sleep(0.5)
                continue
            else:
                try_again = False
        self._password = password

        assert 'user' == xml_user.tag
        l = xml_user.getchildren()
        xml_username = l[1]
        assert 'username' == xml_username.tag
        assert self.is_user_by_name(xml_username.text)

        xml_id = l[0]
        assert 'id' == xml_id.tag
        self.__user_id = int(xml_id.text)

        return True

    def auth_connect(self, url: str, data: str=None, headers: dict or None=None) -> str:
        assert self.__auth_string, "Not auth yet!"
        if headers is None:
            headers = dict()
        headers['Authorization'] = self.__auth_string
        headers['Cookie'] = self.__cookies_string
        sock = _connect(url, data=data, headers=headers)
        return sock.read()

    def is_user_by_name(self, username: str) -> bool:
        return username == self._username

    def is_user_by_id(self, user_id: int) -> bool:
        return user_id == self.__user_id

    @property
    def __cookies_string(self):
        return ";".join(["=".join(item)for item in self.__cookies.items()])

    @property
    def is_auth(self) -> bool:
        return bool(self.__auth_string)

    def __repr__(self):
        return "<Account username: {0:s}>".format(self._username)