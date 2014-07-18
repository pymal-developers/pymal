__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

from urllib import request

from pymal import global_functions
from pymal.types import SingletonFactory
from pymal.consts import HOST_NAME

__all__ = ['Account']


class Account(object, metaclass=SingletonFactory.SingletonFactory):
    """
    """
    __all__ = ['animes', 'mangas', 'reload', 'search', 'auth_connect',
               'connect', 'is_user_by_name', 'is_user_by_id', 'is_auth']
    
    __AUTH_CHECKER_URL =\
        request.urljoin(HOST_NAME, r'api/account/verify_credentials.xml')

    __MY_LOGIN_URL = request.urljoin(HOST_NAME, 'login.php')
    __DATA_FORM = 'username={0:s}&password={1:s}&cookie=1&sublogin=Login'

    def __init__(self, username: str, password: str or None=None):
        """
        """
        from pymal.account_objects import AccountAnimes, AccountMangas

        self.__username = username
        self.__password = password
        self.connect = global_functions.connect
        self.__user_id = None
        self.__auth_object = None
        self.__cookies = dict()

        self.__main_profile_url = request.urljoin(HOST_NAME, 'profile/{0:s}'.format(self.username))
        self.__friends_url = self.__main_profile_url + '/friends'

        self.__animes = AccountAnimes.AccountAnimes(self.username, self)
        self.__mangas = AccountMangas.AccountMangas(self.username, self)
        self.__friends = None

        if password is not None:
            self.change_password(password)

    @property
    def username(self) -> str:
        return self.__username

    @property
    def user_id(self) -> int:
        if self.__user_id is None:
            import bs4

            ret = self.connect(self.__main_profile_url)
            html = bs4.BeautifulSoup(ret)
            bla = html.find(name='input', attrs={'name': 'profileMemId'})
            self.__user_id = int(bla['value'])
        return self.__user_id

    @property
    def mangas(self):
        return self.__mangas

    @property
    def animes(self):
        return self.__animes

    @property
    def friends(self) -> set:
        from pymal.account_objects import AccountFriends

        if self.__friends is None:
            self.__friends = AccountFriends.AccountFriends(self.__friends_url, self)
        return self.__friends

    def search(self, search_line: str, is_anime: bool=True) -> map:
        """
        """
        from pymal import searches

        if is_anime:
            results = searches.search_animes(search_line)
            account_object_list = self.animes
        else:
            results = searches.search_mangas(search_line)
            account_object_list = self.mangas

        def get_object(result):
            if result not in account_object_list:
                return result
            # if account_object_list was set:
            #     return account_object_list.intersection([result]).pop()
            return list(filter(
                lambda x: x == result,
                account_object_list
            ))[0]
        return map(get_object, results)

    def change_password(self, password: str) -> bool:
        """
        Checking if the new password is valid
        """
        from xml.etree import ElementTree
        from requests.auth import HTTPBasicAuth

        self.__auth_object = HTTPBasicAuth(self.username, password)
        data = self.auth_connect(self.__AUTH_CHECKER_URL)
        if data == 'Invalid credentials':
            self.__auth_object = None
            self.__password = None
            return False
        xml_user = ElementTree.fromstring(data)

        assert 'user' == xml_user.tag, 'user == {0:s}'.format(xml_user.tag)
        l = list(xml_user)
        xml_username = l[1]
        assert 'username' == xml_username.tag,\
            'username == {0:s}'.format(xml_username.tag)
        assert self.username == xml_username.text.strip(),\
            'username = {0:s}'.format(xml_username.text.strip())

        xml_id = l[0]
        assert 'id' == xml_id.tag, 'id == {0:s}'.format(xml_id.tag)
        assert self.user_id == int(xml_id.text)

        self.__password = password

        data_form = self.__DATA_FORM.format(self.username, password).encode('utf-8')
        self.connect(self.__MY_LOGIN_URL, data=data_form)

        return True

    def auth_connect(self, url: str, data: str or None=None,
                     headers: dict or None=None) -> str:
        """
        """
        from pymal import exceptions

        if not self.is_auth:
            raise exceptions.UnauthenticatedAccountError(self.username)
        return global_functions._connect(url, data=data, headers=headers,
                                         auth=self.__auth_object).text.strip()

    @property
    def __cookies_string(self) -> str:
        return ";".join(["=".join(item)for item in self.__cookies.items()])

    @property
    def is_auth(self) -> bool:
        """
        """
        return self.__auth_object is not None

    def __repr__(self):
        return "<Account username: {0:s}>".format(self.username)

    def __hash__(self):
        import hashlib

        hash_md5 = hashlib.md5()
        hash_md5.update(self.username.encode())
        return int(hash_md5.hexdigest(), 16)

    def __format__(self, format_spec):
        return str(self).__format__(format_spec)
