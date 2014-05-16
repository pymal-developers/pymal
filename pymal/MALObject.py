import bs4
from pymal.consts import RETRY_NUMBER, RETRY_SLEEP
import time


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



