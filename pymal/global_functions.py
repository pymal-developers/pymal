from urllib import request
import time

import requests
import bs4

from pymal.consts import USER_AGENT, HOST_NAME, RETRY_NUMBER, RETRY_SLEEP

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


def check_side_content_div(expected_text: str, div_node: bs4.element.Tag):
    span_node = div_node.span
    assert span_node is not None, div_node
    expected_text += ":"
    return ['dark_text'] == span_node['class'] and expected_text == span_node.text.strip()


def __get_myanimelist_div(url: str, connection_function) -> bs4.element.Tag:
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


def get_content_wrapper_div(url: str, connection_function) -> bs4.element.Tag:
    myanimelist_div = __get_myanimelist_div(url, connection_function)

    # Getting content wrapper <div>
    content_wrapper_div = myanimelist_div.find(name="div", attrs={"id": "contentWrapper"}, recursive=False)
    assert content_wrapper_div is not None
    return content_wrapper_div
