__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

import hashlib
from xml.etree import ElementTree
from urllib import request

from requests.auth import HTTPBasicAuth
import bs4

from pymal import global_functions
from pymal.types import SingletonFactory
from pymal import consts
from pymal.account_objects import AccountAnimes
from pymal.account_objects import AccountMangas

__all__ = ['Account']


class Account(object, metaclass=SingletonFactory.SingletonFactory):
    """
    """
    __all__ = ['animes', 'mangas', 'reload', 'search', 'auth_connect',
               'connect', 'is_user_by_name', 'is_user_by_id', 'is_auth']
    
    __AUTH_CHECKER_URL =\
        request.urljoin(consts.HOST_NAME, r'api/account/verify_credentials.xml')

    @property
    def __MAIN_PROFILE_URL(self):
        return request.urljoin(consts.HOST_NAME, 'profile/{0:s}'.format(self.username))

    @property
    def __FRIENDS_URL(self):
        return self.__MAIN_PROFILE_URL + '/friends'

    __MY_LOGIN_URL = request.urljoin(consts.HOST_NAME, 'login.php')
    __DATA_FORM = 'username={0:s}&password={1:s}&cookie=1&sublogin=Login'

    def __init__(self, username: str, password: str or None=None):
        """
        """
        self.__username = username
        self.__password = password
        self.connect = global_functions.connect
        self.__user_id = None
        self.__auth_object = None
        self.__cookies = dict()

        self.__animes = None
        self.__mangas = None
        self.__friends = None

        if password is not None:
            self.change_password(password)

    @property
    def username(self) -> str:
        return self.__username

    @property
    def user_id(self) -> int:
        if self.__user_id is None:
            ret = self.connect(self.__MAIN_PROFILE_URL)
            html = bs4.BeautifulSoup(ret)
            bla = html.find(name='input', attrs={'name': 'profileMemId'})
            self.__user_id = int(bla['value'])
        return self.__user_id

    @property
    def mangas(self) -> AccountMangas.AccountMangas:
        if self.__mangas is None:
            self.__mangas = AccountMangas.AccountMangas(self.username, self)
        return self.__mangas

    @property
    def animes(self) -> AccountAnimes.AccountAnimes:
        if self.__animes is None:
            self.__animes = AccountAnimes.AccountAnimes(self.username, self)
        return self.__animes

    @property
    def friends(self) -> set:
        class FriendsFrozenSet(set):
            def __init__(self, account: Account, url: str):
                super().__init__()

                self.account = account
                self.__url = url
                self.reload()

            def reload(self):
                self.clear()
                div_wrapper = global_functions.get_content_wrapper_div(self.__url, self.account.connect)
                assert div_wrapper is not None

                list_div_friend = div_wrapper.findAll(name="div", attrs={"class": "friendBlock"})
                for div_friend in list_div_friend:
                    div_pic = div_friend.find(name="div", attrs={'class': 'picSurround'})
                    assert div_pic is not None

                    splited_friend_url = div_pic.a['href'].split('/profile/', 1)
                    assert len(splited_friend_url) == 2

                    self.add(Account(splited_friend_url[1]))

        self.__friends = FriendsFrozenSet(account=self, url=self.__FRIENDS_URL)
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
        hash_md5 = hashlib.md5()
        hash_md5.update(self.username.encode())
        return int(hash_md5.hexdigest(), 16)
