import bs4
from consts import RETRY_NUMBER
import time

def check_side_content_div(expected_text: str, div_node: bs4.element.Tag):
    span_node = div_node.span
    assert span_node is not None, div_node
    expected_text += ":"
    return ['dark_text'] == span_node['class'] and expected_text == span_node.text


class MALObject(object):
    def _get_myanimelist_div(self, url: str, connection_function) -> bs4.element.Tag:
        got_robot = False
        for try_number in range(RETRY_NUMBER):
            time.sleep(0.5)
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

    def _get_content_wrapper_div(self, url: str, connection_function) -> bs4.element.Tag:
        myanimelist_div = self._get_myanimelist_div(url, connection_function)

        # Getting content wrapper <div>
        content_wrapper_div = myanimelist_div.find(name="div", attrs={"id": "contentWrapper"}, recursive=False)
        assert content_wrapper_div is not None
        return content_wrapper_div