[![Build Status](https://travis-ci.org/tomerghelber/pymal.svg)](https://travis-ci.org/tomerghelber/pymal)
[![Coverage Status](https://coveralls.io/repos/tomerghelber/pymal/badge.png)](https://coveralls.io/r/tomerghelber/pymal)

pymal
==========
Provides programmatic access to MyAnimeList data with python.
Objects in pymal are lazy-loading: they won't go out and fetch MAL info until you first-request it.

This [our doc](http://pymal.rtfd.org).

Dependencies
===========
* `BeautifulSoup4`
    * `html5lib` for BeautifulSoup4 to read html pages better.
* `requests`
    * `httpcache` for requests to have cache (might be removed because no cache can be created with mal right now).
* `pillows`
 To show users' avatars and mangas/animes icon.

Installation
============
After cloning the repository, navigate to the directory and run `python setup.py install`.
