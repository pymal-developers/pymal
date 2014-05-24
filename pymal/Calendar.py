from urllib import request
import datetime
import bs4
import dateutils
import icalendar
import requests
from pymal.decorators import load


class Calendar(object):
    HOST_NAME = 'http://animecalendar.net'
    QUERY_CALENDAR = "%Y/%m"
    DATE_FORMAT = '/%Y/%m/%d'
    TIME_FORMAT = '(%H:%M)'
    EPISODE_TIME = dateutils.relativedelta(minutes=30)

    def __init__(self):
        self.__ical = icalendar.Calendar()
        self.__ical.add('summary', 'Calendar of transmission times of Anime')
        self._is_loaded = False

    @property
    @load
    def ical(self):
        return self.__ical

    def __parse_episode_cell(self, date_string: str, episode: bs4.element.Tag):
        anime_name = episode.h3.text.strip()
        episode_data = episode.small.text
        _, number, time, _ = episode_data.splitlines()
        number = int(number.split('Ep: ')[1])
        start_date = datetime.datetime.strptime(date_string + ' ' + time.strip(), self.DATE_FORMAT + ' ' + self.TIME_FORMAT)
        end_date = start_date + self.EPISODE_TIME

        event = icalendar.Event()
        event.add('dtstart', start_date)
        event.add('dtend', end_date)
        event.add('summary', anime_name)
        event.add('comment ', number)
        self.__ical.add_component(event)

    def __parse_day_html(self, cell: bs4.element.Tag) -> bool:
        cell = cell.div
        if cell is None:
            return False

        cell = cell.table
        date_string = cell.thead.tr.th.h2.a['href']
        episode_cells = cell.tbody.findAll(name='tr', recursive=False)
        if len(episode_cells) == 0:
            return False

        for episode_cell in episode_cells:
            episode = episode_cell.find(name="div", attrs={'class': "ep_box"})
            assert episode is not None, 'type(episode)=' + type(episode) + 'str(episode_cell)=' + str(episode_cell)
            self.__parse_episode_cell(date_string, episode)
        return True

    def __parse_week_html(self, row: bs4.element.Tag):
        row_list = list(row)
        assert 7 == len(row_list)
        return any([self.__parse_day_html(cell) for cell in row_list])

    def __parse_calendar_html(self, calendar_url: str) -> bool:
        html = bs4.BeautifulSoup(requests.get(calendar_url).text)
        calendar_div = html.find(name="div", attrs={"id": "calendarContent"})
        assert calendar_div is not None
        calendar_table = calendar_div.find(name='table', recursive=False)
        assert calendar_table is not None, type(calendar_table)

        calendar_table_head = calendar_table.thead.tr
        calendar_header = [i.text for i in calendar_table_head.findAll(name="th", recursive=False)]
        assert 7 == len(calendar_header)

        return any([self.__parse_week_html(row) for row in calendar_table.tbody.findAll(name="tr", recursive=False)])

    def reload(self):
        now_datetime = datetime.datetime.now()
        month_jumps = dateutils.relativedelta(months=1)
        while self.__parse_calendar_html(request.urljoin(self.HOST_NAME, now_datetime.strftime(self.QUERY_CALENDAR))):
            now_datetime += month_jumps
