import json
from os import path


TEST_SETTINGS = path.join(path.dirname(__file__), "account_settings.json")
__settings_dict = json.load(open(TEST_SETTINGS, "r"))
ACCOUNT_TEST_USERNAME = __settings_dict['username']
ACCOUNT_TEST_PASSWORD = __settings_dict['password']

ANIME_ID = 1887
MANGA_ID = 587
