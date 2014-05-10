import json
from os import path


TEST_SETTINGS = path.join(path.dirname(__file__), "account_settings.json")
ACCOUNT_TEST_USERNAME, ACCOUNT_TEST_PASSWORD = json.load(open(TEST_SETTINGS, "r")).values()

ANIME_ID = 1887
MANGA_ID = 587
