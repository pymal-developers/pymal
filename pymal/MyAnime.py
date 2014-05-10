from urllib import request
from pymal.consts import HOST_NAME
from pymal.decorators import my_load
from pymal.Anime import Anime


class MyAnime(Anime):
    MY_ANIME_URL = request.urljoin(HOST_NAME, 'editlist.php?type=anime&id={0:d}')
    MY_ANIME_EPISODES_URL = request.urljoin(HOST_NAME, 'ajaxtb.php?detailedaid={0:d}')
    MY_LOGIN_URL = request.urljoin(HOST_NAME, 'login.php')
    TAG_SEPARETOR = ';'

    MY_ANIME_DELETE_URL = request.urljoin(HOST_NAME, 'api/animelist/delete/{0:d}.xml')
    MY_ANIME_UPDATE_URL = request.urljoin(HOST_NAME, 'api/animelist/update/{0:d}.xml')

    def __init__(self, anime_id: int or Anime, account, my_xml: None=None):
        if type(anime_id) == Anime:
            anime_id = anime_id.anime_id
        super().__init__(anime_id, anime_xml=my_xml)

        self.__my_anime_url = self.MY_ANIME_URL.format(self._anime_id)

        self._is_my_loaded = False
        self.__account = account

        self.__my_id = None
        self.__my_status = None
        self.__my_is_rewatching = None
        self.__my_completed_episodes = None
        self.__my_score = None
        self.__my_start_date = None
        self.__my_end_date = None
        self.__my_priority = 0
        self.__my_storage_type = 0
        self.__my_storage_value = 0.0
        self.__my_download_episodes = 0
        self.__my_times_rewatched = 0
        self.__my_rewatch_value = None
        self.__my_tags = None

        if my_xml is not None:
            self.__my_id = int(my_xml.find('my_id').text.strip())
            self.__my_status = int(my_xml.find('my_status').text.strip())
            if my_xml.find('my_rewatching').text is not None:
                self.__my_is_rewatching = bool(int(my_xml.find('my_rewatching').text.strip()))
            self.__my_completed_episodes = int(my_xml.find('my_watched_episodes').text.strip())
            self.__my_score = int(my_xml.find('my_score').text.strip())
            self.__my_start_date = my_xml.find('my_start_date').text.strip()
            self.__my_end_date = my_xml.find('my_finish_date').text.strip()
            self.__my_rewatch_value = int(my_xml.find('my_rewatching_ep').text.strip())
            my_tags_xml = my_xml.find('my_tags')
            if my_tags_xml.text is not None:
                self.__my_tags = my_tags_xml.text.strip().split(self.TAG_SEPARETOR)


    @property
    def my_id(self):
        return self.__my_id

    @property
    def my_status(self):
        if self.__my_status is None:
            self.my_reload()
        return self.__my_status

    @property
    def my_is_rewatching(self):
        if self.__my_is_rewatching is None:
            self.my_reload()
        return self.__my_is_rewatching

    @property
    def my_completed_episodes(self):
        if self.__my_completed_episodes is None:
            self.my_reload()
        return self.__my_completed_episodes

    @property
    def my_score(self):
        if self.__my_score is None:
            self.my_reload()
        return self.__my_score

    @property
    def my_start_date(self):
        if self.__my_start_date is None:
            self.my_reload()
        return self.__my_start_date

    @property
    def my_end_date(self):
        if self.__my_end_date is None:
            self.my_reload()
        return self.__my_end_date

    @property
    @my_load
    def my_priority(self):
        return self.__my_priority

    @property
    @my_load
    def my_storage_type(self):
        return self.__my_storage_type

    @property
    @my_load
    def my_storage_value(self):
        return self.__my_storage_value

    @property
    @my_load
    def my_download_episodes(self):
        return self.__my_download_episodes

    @property
    def my_times_rewatched(self):
        if self.__my_times_rewatched is None:
            self.my_reload()
        return self.__my_times_rewatched

    @property
    def my_rewatch_value(self):
        if self.__my_rewatch_value is None:
            self.my_reload()
        return self.__my_rewatch_value

    def my_reload(self):
        # Getting content wrapper <div>
        content_wrapper_div = self._get_content_wrapper_div(self.__my_anime_url, self.__account.auth_connect)

        #Getting content <td>
        content_div = content_wrapper_div.find(name="div", attrs={"id": "content"}, recursive=False)
        assert content_div is not None

        content_td = content_div.table.tr.td
        assert content_div is not None

        #Getting content <div>
        content_td_divs = content_td.findAll(name="div", recursive=False)
        if 0 == len(content_td_divs):
            data_form = 'username={0:s}&password={1:s}&sublogin=Login'
            data_form = data_form .format(self.__account._username, self.__account._password)
            data_form = data_form.encode('utf-8')

            self.__account.auth_connect(self.MY_LOGIN_URL, data=data_form)

            # Getting content wrapper <div>
            content_wrapper_div = self._get_content_wrapper_div(self.__my_anime_url, self.__account.auth_connect)
            #Getting content <td>
            content_div = content_wrapper_div.find(name="div", attrs={"id": "content"}, recursive=False)


            content_td = content_div.table.tr.td
            assert content_div is not None

            #Getting content <div>
            content_td_divs = content_td.findAll(name="div", recursive=False)
            assert 2 == len(content_td_divs), "Got len(content_td_divs) == {0:d}".format(len(content_td_divs))

        content_div = content_td_divs[1]

        #Getting content rows <tr>
        content_form = content_div.form
        assert 'myAnimeForm' == content_form['id'], "Got content_form['id'] == {0:s}".format(content_form['id'])
        content_rows = content_form.table.tbody.findAll(name="tr", recursive=False)

        # Getting my_status
        status_select = content_rows[3].find(name="select", attrs={"id": "status", "name": "status"})
        assert status_select is not None
        status_selected_option = status_select.find(name="option", attrs={"selected": ""})
        assert status_selected_option is not None
        self.__my_status = int(status_selected_option['value'])
        is_rewatch_node = content_rows[3].find(name="input", attrs={"id": "rewatchingBox"})
        assert is_rewatch_node is not None
        self.__my_is_rewatching = bool(is_rewatch_node['value'])

        # Getting watched episodes
        watched_input = content_rows[4].find(name="input", attrs={"id": "completedEpsID", "name": "completed_eps"})
        assert watched_input is not None
        self.__my_completed_episodes = int(watched_input['value'])

        # Getting my_score
        score_select = content_rows[5].find(name="select", attrs={"id": "inputtext", "name": "score"})
        assert score_select is not None
        score_selected_option = score_select.find(name="option", attrs={"selected": ""})
        assert score_selected_option is not None
        self.__my_score = int(score_selected_option['value'])

        # Getting my_tags...
        tag_content = content_rows[6]

        # Getting start date
        start_month_date_node = content_rows[7].find(name="select", attrs={"name": "startMonth"})
        assert start_month_date_node is not None
        start_day_date = content_rows[7].find(name="select", attrs={"name": "startDay"})
        assert start_day_date is not None
        start_year_date = content_rows[7].find(name="select", attrs={"name": "startYear"})
        assert start_year_date is not None
        start_month_date = str(start_month_date_node).zfill(2)
        start_day_date = str(start_day_date).zfill(2)
        start_year_date = str(start_year_date).zfill(2)
        self.__my_start_date = start_month_date + start_day_date + start_year_date

        # Getting end date
        end_month_date_node = content_rows[8].find(name="select", attrs={"name": "endMonth"})
        assert end_month_date_node is not None
        end_day_date = content_rows[8].find(name="select", attrs={"name": "endDay"})
        assert end_day_date is not None
        end_year_date = content_rows[8].find(name="select", attrs={"name": "endYear"})
        assert end_year_date is not None
        end_month_date = str(end_month_date_node).zfill(2)
        end_day_date = str(end_day_date).zfill(2)
        end_year_date = str(end_year_date).zfill(2)
        self.__my_end_date = end_month_date + end_day_date + end_year_date

        # Getting fansub group
        # content_rows[9]

        # Getting priority
        priority_node = content_rows[10].find(name="select", attrs={"name": "priority"})
        assert priority_node is not None
        selected_priority_node = priority_node.find(name="option", attrs={"selected": ""})
        assert selected_priority_node is not None
        self.__my_priority = selected_priority_node['value']

        # Getting storage
        storage_type_node = content_rows[11].find(name="select", attrs={"id": "storage"})
        assert storage_type_node is not None
        selected_storage_type_node = storage_type_node.find(name="option", attrs={"selected": ""})
        assert selected_storage_type_node is not None
        self.__my_storage_type = selected_storage_type_node['value']

        storage_value_node = content_rows[11].find(name="input", attrs={"id": "storageValue"})
        assert storage_value_node is not None
        self.__my_storage_value = float(storage_value_node['value'])

        # Getting downloaded episodes
        download_episodes_node = content_rows[12].find(name="input", attrs={'id': "epDownloaded", 'name': 'list_downloaded_eps'})
        assert download_episodes_node is not None
        self.__my_download_episodes == int(download_episodes_node['value'])

        # Getting time rewatched
        times_rewatched_node = content_rows[13].find(name="input", attrs={'name': 'list_times_watched'})
        self.__my_times_rewatched == int(times_rewatched_node['value'])
        assert times_rewatched_node is not None

        # Getting rewatched value
        rewatch_value_node = content_rows[14].find(name="select", attrs={'name': 'list_rewatch_value'})
        assert rewatch_value_node is not None
        rewatch_value_option = rewatch_value_node.find(name='option', attrs={'selected': ''})
        assert rewatch_value_option is not None
        self.__my_rewatch_value == int(rewatch_value_option['value'])

        # Getting comments
        content_rows[15]

        # Getting discuss flag
        discuss_node = content_rows[16].find(name='select', attrs={"name": "discuss"})
        assert discuss_node is not None
        self._is_my_loaded = True