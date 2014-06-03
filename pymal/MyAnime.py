__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

import hashlib
from urllib import request
import time

from pymal import consts
from pymal import decorators
from pymal import Anime
from pymal import global_functions

__all__ = ['MyAnime']


class MyAnime(object, metaclass=decorators.SingletonFactory):
    """
    Saves an account data about anime.
    
    Attributes:
        my_enable_discussion - boolean
        my_id - int
        my_status - int.  #TODO: put the dictanary here.
        my_score - int.
        my_start_date - string as mmddyyyy.
        my_end_date - string as mmddyyyy.
        my_priority - int.
        my_storage_type - int.  #TODO: put the dictanary here.
        my_storage_value - float.
        my_is_rereading - boolean.
        my_completed_episodes - int.
        my_download_episodes - int.
        my_times_reread - int.
        my_reread_value - int.
        my_tags - string.
        my_comments - string
        my_fan_sub_groups - string.
    """
    __all__ = ['my_enable_discussion', 'my_id', 'my_status', 'my_score',
               'my_start_date', 'my_end_date', 'my_priority',
               'my_storage_type', 'my_storage_value', 'my_is_rewatching',
               'my_completed_episodes', 'my_score', 'my_download_episodes',
               'my_times_rewatched', 'my_rewatch_value',
               'my_tags', 'my_comments', 'my_fan_sub_groups', 'my_reload',
               'update', 'delete']

    __TAG_SEPARATOR = ';'
    __MY_MAL_URL = request.urljoin(
        consts.HOST_NAME, 'editlist.php?type=anime&id={0:d}')
    __MY_MAL_DELETE_URL = request.urljoin(
        consts.HOST_NAME, 'api/animelist/delete/{0:d}.xml')
    __MY_MAL_UPDATE_URL = request.urljoin(
        consts.HOST_NAME, 'api/animelist/update/{0:d}.xml')

    def __init__(self, mal_id: int or Anime.Anime, my_mal_id, account,
                 my_mal_xml: None=None):
        """
        """
        if isinstance(mal_id, Anime.Anime):
            self.obj = mal_id
        else:
            self.obj = Anime.Anime(mal_id, mal_xml=my_mal_xml)

        self.__my_mal_url = self.__MY_MAL_URL.format(self.obj.id)

        self._is_my_loaded = False
        self._account = account

        self.__my_mal_id = my_mal_id
        self.__my_status = None
        self.my_enable_discussion = False
        self.__my_score = None
        self.__my_start_date = None
        self.__my_end_date = None
        self.__my_priority = 0
        self.__my_storage_type = 0
        self.__my_storage_value = 0.0
        self.__my_comments = ''
        self.__my_fan_sub_groups = ''
        self.__my_tags = None

        self.__my_is_rewatching = None
        self.__my_completed_episodes = None
        self.__my_download_episodes = 0
        self.__my_times_rewatched = 0
        self.__my_rewatch_value = None

        if my_mal_xml is not None:
            self.__my_id = int(my_mal_xml.find('my_id').text.strip())
            self.__my_status = int(my_mal_xml.find('my_status').text.strip())
            if my_mal_xml.find('my_rewatching').text is not None:
                self.__my_is_rewatching = bool(
                    int(my_mal_xml.find('my_rewatching').text.strip()))
            else:
                self.__my_is_rewatching = False
            self.__my_completed_episodes = int(
                my_mal_xml.find('my_watched_episodes').text.strip())
            self.__my_score = int(my_mal_xml.find('my_score').text.strip())
            my_start_date = my_mal_xml.find('my_start_date').text.strip()
            if my_start_date == consts.MALAPPINFO_NONE_TIME:
                self.__my_start_date = consts.MALAPI_NONE_TIME
            else:
                my_start_date = time.strptime(
                    my_start_date, consts.MALAPPINFO_FORMAT_TIME)
                self.__my_start_date = time.strftime(
                    consts.MALAPI_FORMAT_TIME, my_start_date)
            my_end_date = my_mal_xml.find('my_finish_date').text.strip()
            if my_end_date == consts.MALAPPINFO_NONE_TIME:
                self.__my_end_date = consts.MALAPI_NONE_TIME
            else:
                my_end_date = time.strptime(
                    my_end_date, consts.MALAPPINFO_FORMAT_TIME)
                self.__my_end_date = time.strftime(
                    consts.MALAPI_FORMAT_TIME, my_end_date)
            self.__my_rewatch_value = int(
                my_mal_xml.find('my_rewatching_ep').text.strip())
            my_tags_xml = my_mal_xml.find('my_tags')
            if my_tags_xml.text is None:
                self.__my_tags = ''
            else:
                self.__my_tags = my_tags_xml.text.strip().split(
                    self.__TAG_SEPARATOR)

    @property
    def my_id(self):
        return self.__my_mal_id

    @property
    def my_status(self):
        if self.__my_status is None:
            self.my_reload()
        return self.__my_status

    @my_status.setter
    def my_status(self, value: int):
        if not (1 <= value <= 6):
            raise RuntimeError("value of my_statue can be 1 to 6")
        self.__my_status = value

    @property
    def my_score(self):
        if self.__my_score is None:
            self.my_reload()
        return self.__my_score

    @my_score.setter
    def my_score(self, value: int):
        if not (0 <= value <= 10):
            raise RuntimeError("value of my_score can be 0 to 10")
        self.__my_score = value

    @property
    def my_start_date(self):
        if self.__my_start_date is None:
            self.my_reload()
        return self.__my_start_date

    @my_start_date.setter
    def my_start_date(self, value: str):
        time.strptime(value, consts.MALAPI_FORMAT_TIME)
        self.__my_start_date = value

    @property
    def my_end_date(self):
        if self.__my_end_date is None:
            self.my_reload()
        return self.__my_end_date

    @my_end_date.setter
    def my_end_date(self, value: str):
        time.strptime(value, consts.MALAPI_FORMAT_TIME)
        self.__my_end_date = value

    @property
    @decorators.my_load
    def my_priority(self):
        return self.__my_priority

    @my_priority.setter
    def my_priority(self, value: int):
        if not (0 <= value <= 3):
            raise RuntimeError("value of my_priority can be 0 to 3")
        self.__my_priority = value

    @property
    @decorators.my_load
    def my_storage_type(self):
        return self.__my_storage_type

    @my_storage_type.setter
    def my_storage_type(self, value: int):
        if not (0 <= value <= 7):
            raise RuntimeError("value of my_storage_type can be 0 to 7")
        self.__my_storage_type = value

    @property
    @decorators.my_load
    def my_storage_value(self):
        return self.__my_storage_value

    @my_storage_type.setter
    def my_storage_value(self, value: float):
        int(value)
        self.__my_storage_value = value

    @property
    def my_is_rewatching(self):
        if self.__my_is_rewatching is None:
            self.my_reload()
        return self.__my_is_rewatching

    @my_is_rewatching.setter
    def my_is_rewatching(self, value: bool):
        self.__my_is_rewatching = value

    @property
    def my_completed_episodes(self):
        if self.__my_completed_episodes is None:
            self.my_reload()
        return self.__my_completed_episodes

    @my_completed_episodes.setter
    def my_completed_episodes(self, value: int):
        if not (0 <= value <= self.episodes):
            raise RuntimeError("value of my_completed_episodes can be 0 to self.episodes")
        self.__my_completed_episodes = value

    @property
    @decorators.my_load
    def my_download_episodes(self):
        return self.__my_download_episodes

    @my_download_episodes.setter
    def my_download_episodes(self, value: int):
        if not (0 <= value <= self.episodes):
            raise RuntimeError("value of my_download_episodes can be 0 to self.episodes")
        self.__my_download_episodes = value

    @property
    def my_times_rewatched(self):
        if self.__my_times_rewatched is None:
            self.my_reload()
        return self.__my_times_rewatched

    @my_times_rewatched.setter
    def my_times_rewatched(self, value: int):
        if not (0 <= value):
            raise RuntimeError("value of my_times_rewatched can be 0 or more")
        self.__my_times_rewatched = value

    @property
    def my_rewatch_value(self):
        if self.__my_rewatch_value is None:
            self.my_reload()
        return self.__my_rewatch_value

    @my_rewatch_value.setter
    def my_rewatch_value(self, value: int):
        if not (0 <= value <= 5):
            raise RuntimeError("value of my_rewatch_value can be 0 to 5")
        self.__my_rewatch_value = value

    @property
    def my_tags(self):
        if self.__my_tags is None:
            self.my_reload()
        return self.__my_tags

    @property
    @decorators.my_load
    def my_comments(self):
        return self.__my_comments

    @property
    @decorators.my_load
    def my_fan_sub_groups(self):
        return self.__my_fan_sub_groups

    def my_reload(self):
        # Getting content wrapper <div>
        content_wrapper_div = global_functions.get_content_wrapper_div(
            self.__my_mal_url, self._account.auth_connect)

        bas_result = content_wrapper_div.find(name='div',
                                              attrs={'class': 'badresult'})
        assert bas_result is not None

        # Getting content <td>
        content_div = content_wrapper_div.find(
            name="div", attrs={"id": "content"}, recursive=False)
        assert content_div is not None

        content_td = content_div.table.tr.td
        assert content_td is not None

        # Getting content rows <tr>
        content_form = content_td.find(name="form", attrs={'id': "myAnimeForm"})
        assert 'myAnimeForm' == content_form['id'], content_form['id']
        content_rows = content_form.table.tbody.findAll(
            name="tr", recursive=False)

        contents_divs_index = 2

        # Getting my_status
        status_select = content_rows[contents_divs_index].find(
            name="select", attrs={"id": "status", "name": "status"})
        assert status_select is not None
        # TODO: make this look better
        status_selected_options = [
            x
            for x in status_select.findAll(name="option")
            if 'selected' in x.attrs
        ]
        assert 1 == len(status_selected_options)
        self.__my_status = int(status_selected_options[0]['value'])

        is_rewatch_node = content_rows[contents_divs_index].find(
            name="input", attrs={"id": "rewatchingBox"})
        assert is_rewatch_node is not None
        self.__my_is_rewatching = bool(is_rewatch_node['value'])
        contents_divs_index += 1

        # Getting watched episodes
        watched_input = content_rows[contents_divs_index].\
            find(name="input", attrs={"id": "completedEpsID",
                                      "name": "completed_eps"})
        assert watched_input is not None
        self.__my_completed_episodes = int(watched_input['value'])
        contents_divs_index += 1

        # Getting my_score
        score_select = content_rows[contents_divs_index].find(
            name="select", attrs={"name": "score"})
        assert score_select is not None
        score_selected_option = score_select.find(
            name="option", attrs={"selected": ""})
        assert score_selected_option is not None
        self.__my_score = int(float(score_selected_option['value']))
        contents_divs_index += 1

        # Getting my_tags...
        tag_content = content_rows[contents_divs_index]
        tag_textarea = tag_content.find(
            name="textarea", attrs={"name": "tags"})
        self.__my_tags = tag_textarea.text
        contents_divs_index += 1

        # Getting start date
        start_month_date_node = content_rows[contents_divs_index].find(
            name="select", attrs={"name": "startMonth"})
        assert start_month_date_node is not None
        start_month_date = start_month_date_node.find(
            name="option", attrs={"selected": ""})

        start_day_date_node = content_rows[contents_divs_index].find(
            name="select", attrs={"name": "startDay"})
        assert start_day_date_node is not None
        start_day_date = start_day_date_node.find(
            name="option", attrs={"selected": ""})

        start_year_date_node = content_rows[contents_divs_index].find(
            name="select", attrs={"name": "startYear"})
        assert start_year_date_node is not None
        start_year_date = start_year_date_node.find(
            name="option", attrs={"selected": ""})

        start_month_date = str(start_month_date['value']).zfill(2)
        start_day_date = str(start_day_date['value']).zfill(2)
        start_year_date = str(start_year_date['value']).zfill(2)
        self.__my_start_date = start_month_date + \
            start_day_date + start_year_date
        contents_divs_index += 1

        # Getting end date
        end_month_date_node = content_rows[contents_divs_index].find(
            name="select", attrs={"name": "endMonth"})
        assert end_month_date_node is not None
        end_month_date = end_month_date_node.find(
            name="option", attrs={"selected": ""})

        end_day_date_node = content_rows[contents_divs_index].find(
            name="select", attrs={"name": "endDay"})
        assert end_day_date_node is not None
        end_day_date = end_day_date_node.find(
            name="option", attrs={"selected": ""})

        end_year_date_node = content_rows[contents_divs_index].find(
            name="select", attrs={"name": "endYear"})
        assert end_year_date_node is not None
        end_year_date = end_year_date_node.find(
            name="option", attrs={"selected": ""})

        end_month_date = str(end_month_date['value']).zfill(2)
        end_day_date = str(end_day_date['value']).zfill(2)
        end_year_date = str(end_year_date['value']).zfill(2)
        self.__my_end_date = end_month_date + end_day_date + end_year_date
        contents_divs_index += 1

        # Getting fansub group
        fansub_group_content = content_rows[contents_divs_index]
        fansub_group_input = fansub_group_content.find(
            name="input", attrs={"name": "fansub_group"})
        self.__my_fan_sub_groups = fansub_group_input.text
        contents_divs_index += 1

        # Getting priority
        priority_node = content_rows[contents_divs_index].find(
            name="select", attrs={"name": "priority"})
        assert priority_node is not None
        selected_priority_node = priority_node.find(
            name="option", attrs={"selected": ""})
        assert selected_priority_node is not None
        self.__my_priority = int(selected_priority_node['value'])
        contents_divs_index += 1

        # Getting storage
        storage_type_node = content_rows[contents_divs_index].find(
            name="select", attrs={"id": "storage"})
        assert storage_type_node is not None
        selected_storage_type_node = storage_type_node.find(
            name="option", attrs={"selected": ""})
        assert selected_storage_type_node is not None
        self.__my_storage_type = int(selected_storage_type_node['value'])

        storage_value_node = content_rows[contents_divs_index].find(
            name="input", attrs={"id": "storageValue"})
        assert storage_value_node is not None
        self.__my_storage_value = float(storage_value_node['value'])
        contents_divs_index += 1

        # Getting downloaded episodes
        downloaded_episodes_node = content_rows[contents_divs_index].\
            find(name="input", attrs={'id': "epDownloaded",
                                      'name': 'list_downloaded_eps'})
        assert downloaded_episodes_node is not None
        self.__my_download_episodes == int(downloaded_episodes_node['value'])
        contents_divs_index += 1

        # Getting time rewatched
        times_rewatched_node = content_rows[contents_divs_index].find(
            name="input", attrs={'name': 'list_times_watched'})
        self.__my_times_rewatched == int(times_rewatched_node['value'])
        assert times_rewatched_node is not None
        contents_divs_index += 1

        # Getting rewatched value
        rewatch_value_node = content_rows[contents_divs_index].find(
            name="select", attrs={'name': 'list_rewatch_value'})
        assert rewatch_value_node is not None
        rewatch_value_option = rewatch_value_node.find(
            name='option', attrs={'selected': ''})
        assert rewatch_value_option is not None
        self.__my_rewatch_value = int(rewatch_value_option['value'])
        contents_divs_index += 1

        # Getting comments
        comment_content = content_rows[contents_divs_index]
        comment_textarea = comment_content.find(
            name="textarea", attrs={"name": "list_comments"})
        self.__my_comments = comment_textarea.text
        contents_divs_index += 1

        # Getting discuss flag
        discuss_node = content_rows[contents_divs_index].find(
            name='select', attrs={"name": "discuss"})
        assert discuss_node is not None
        self._is_my_loaded = True

    def to_xml(self):
        data = self.MY_MAL_XML_TEMPLATE.format(
            self.my_completed_episodes,
            self.my_status,
            self.my_score,
            self.my_download_episodes,
            self.my_storage_type,
            self.my_storage_value,
            self.my_times_rewatched,
            self.my_rewatch_value,
            self.my_start_date,
            self.my_end_date,
            self.my_priority,
            self.my_enable_discussion,
            self.my_is_rewatching,
            self.my_comments,
            self.my_fan_sub_groups,
            self.my_tags
        )
        return data

    def add(self, account):
        if account == self._account:
            return self
        return self.obj.add(account)

    def update(self):
        """
        """
        self.ret_data = self._account.auth_connect(
            self.__MY_MAL_UPDATE_URL.format(self.id), data=self.to_xml())
        print(self.ret_data)
        assert self.ret_data == 'Updated'

    def delete(self):
        """
        """
        self.ret_data = self._account.auth_connect(
            self.__MY_MAL_DELETE_URL.format(self.id), data='')
        print(self.ret_data)
        assert self.ret_data == 'Deleted'

    def increase(self) -> bool:
        if self.is_completed:
            return False
        self.my_completed_episodes += 1
        return True

    def increase_downloaded(self) -> bool:
        if self.is_completed:
            return False
        self.my_download_episodes += 1
        return True

    @property
    def is_completed(self) -> bool:
        return self.my_completed_episodes >= self.obj.episodes

    def set_completed(self) -> bool:
        if self.obj.episodes == float('inf'):
            return False
        self.my_completed_episodes = self.obj.episodes
        return True

    def set_completed_download(self) -> bool:
        if self.obj.episodes == float('inf'):
            return False
        self.my_download_episodes = self.obj.episodes
        return True

    def __getattr__(self, name):
        return getattr(self.obj, name)

    def __dir__(self):
        return list(set(dir(type(self)) + list(self.__dict__.keys()) + dir(self.obj)))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return hash(other) == hash(self)
        if isinstance(other, self.obj.__class__):
            return hash(other) == hash(self.obj)
        return False

    def __hash__(self):
        hash_md5 = hashlib.md5()
        hash_md5.update(str(self.id).encode())
        hash_md5.update(str(hash(self._account)).encode())
        hash_md5.update(b'MyAnime')
        return int(hash_md5.hexdigest(), 16)

    def __repr__(self):
        title = " '{0:s}'".format(self.title) if self.obj._is_loaded else ''
        return "<{0:s}{1:s} of account '{2:s}' id={3:d}>".format(
            self.__class__.__name__, title, self._account._username, self.id)
