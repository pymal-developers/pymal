from pymal.consts import USER_AGENT, HOST_NAME
import requests
from urllib import request


__SESSION = requests.session()


def url_fixer(url: str) -> str:
    url = url.encode('utf-8')
    for i in range(128, 256):
        url = url.replace(bytes([i]), '%{0:X}'.format(i).encode("utf-8"))
    return url.decode('utf-8')


def _connect(url: str, data: str=None, headers: dict or None=None, auth=None) -> requests.Response:
    """
    :param url: url
    :param data: data to post
    :param headers: headers to send
    :rtype : responded sock
    """
    if headers is None:
        headers = dict()

    url = url_fixer(url)

    headers['User-Agent'] = USER_AGENT
    if data is not None:
        sock = __SESSION.post(url, data=data, headers=headers, auth=auth)
    else:
        sock = __SESSION.get(url, headers=headers, auth=auth)
    return sock


def connect(url: str, data: str=None, headers: dict or None=None, auth=None) -> str:
    """
    :param url: url
    :param data: data to post
    :param headers: headers to send
    :rtype : responded data
    """
    return _connect(url, data, headers, auth).text.strip()


def get_next_index(i: int, list_of_tags: list) -> int:
    """
    return the i after the next <br/>

    :type i: int
    :param i: an index
    :type list_of_tags: list
    :param list_of_tags: list of tags to check the i on
    :rtype: int
    """
    while i < len(list_of_tags) and list_of_tags[i].name != 'br':
        i += 1
    return i + 1


def make_list(self_list: list, i: int, list_of_tags: list) -> int:
    """
    return the index after the next <br/> and inserting all the link until it.

    :type self_list: list
    :param self_list: a list to append links to
    :type i: int
    :param i: an index
    :type list_of_tags: list
    :param list_of_tags: list of tags to check the index on
    :rtype: int
    """
    # TODO: find a way to put it out
    from pymal.Anime import Anime
    from pymal.Manga import Manga

    n_i = get_next_index(i, list_of_tags)
    for i in range(i + 1, n_i, 2):
        assert 'a' == list_of_tags[i].name, list_of_tags[i].name
        if '/anime/' in list_of_tags[i]['href']:
            self_list.append(Anime(int(list_of_tags[i]['href'].split('/anime/')[1].split('/')[0])))
        elif '/manga/' in list_of_tags[i]['href']:
            self_list.append(Manga(int(list_of_tags[i]['href'].split('/manga/')[1].split('/')[0])))
        else:
            self_list.append(request.urljoin(HOST_NAME, list_of_tags[i]['href']))
    return n_i