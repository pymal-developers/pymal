from xml.etree import ElementTree
from global_functions import _connect
from decorators import load
from AccountAnimes import AccountAnimes
from AccountMangas import AccountMangas
from requests.auth import HTTPBasicAuth


class Account(object):
    AUTH_CHECKER_URL = r'http://myanimelist.net/api/account/verify_credentials.xml'

    def __init__(self, username: str, password: str or None=None):
        self._username = username
        self.__user_id = 0
        self.__auth_object = None
        self.__cookies = dict()

        self._is_loaded = False
        self.__animes = None
        self.__mangas = None

        if password is not None:
            self.change_password(password)

    @property
    @load
    def animes(self):
        return self.__animes

    @property
    @load
    def mangas(self):
        return self.__mangas

    def reload(self):
        self.__animes = AccountAnimes(self._username, self)
        self.__mangas = AccountMangas(self._username, self)
        self._is_loaded = True

    def change_password(self, password: str) -> bool:
        """Checking if the new password is valid"""
        self.__auth_object = HTTPBasicAuth(self._username, password)
        data = self.auth_connect(self.AUTH_CHECKER_URL)
        if data == 'Invalid credentials':
            self.__auth_object = None
            return False
        xml_user = ElementTree.fromstring(data)

        assert 'user' == xml_user.tag, 'user == {0:s}'.format(xml_user.tag)
        l = xml_user.getchildren()
        xml_username = l[1]
        assert 'username' == xml_username.tag, 'username == {0:s}'.format(xml_username.tag)
        assert self.is_user_by_name(xml_username.text.strip()), 'username = {0:s}'.format(xml_username.text.strip())

        xml_id = l[0]
        assert 'id' == xml_id.tag, 'id == {0:s}'.format(xml_id.tag)
        self.__user_id = int(xml_id.text.strip())

        return True

    def auth_connect(self, url: str, data: str=None, headers: dict or None=None) -> str:
        assert self.__auth_object is not None, "Not auth yet!"
        if headers is None:
            headers = dict()
        return _connect(url, data=data, headers=headers, auth=self.__auth_object).text.strip()

    def is_user_by_name(self, username: str) -> bool:
        return username == self._username

    def is_user_by_id(self, user_id: int) -> bool:
        return user_id == self.__user_id

    @property
    def __cookies_string(self):
        return ";".join(["=".join(item)for item in self.__cookies.items()])

    @property
    def is_auth(self) -> bool:
        return self.__auth_object is not None

    def __repr__(self):
        return "<Account username: {0:s}>".format(self._username)