.. pymal documentation master file, created by
   sphinx-quickstart on Fri Sep 19 13:23:51 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pymal's documentation!
=================================

|BuildStatus|_ |CoverageStatus|_ |DevelopmentStatus|_

|SupportedPythonversions|_ |SupportedPythonimplementations|_

|Downloads|_ |LatestVersion|_ |License|_

.. |BuildStatus| image:: https://travis-ci.org/tomerghelber/pymal.svg
.. _BuildStatus: https://travis-ci.org/tomerghelber/pymal/
.. |CoverageStatus| image:: https://coveralls.io/repos/tomerghelber/pymal/badge.png
.. _CoverageStatus: https://coveralls.io/r/tomerghelber/pymal/
.. |DevelopmentStatus| image:: https://pypip.in/status/pymal/badge.svg
.. _DevelopmentStatus: https://pypi.python.org/pypi/pymal/

.. |SupportedPythonversions| image:: https://pypip.in/py_versions/pymal/badge.svg
.. _SupportedPythonversions: https://pypi.python.org/pypi/pymal/
.. |SupportedPythonimplementations| image:: https://pypip.in/implementation/pymal/badge.svg
.. _SupportedPythonimplementations: https://pypi.python.org/pypi/pymal/

.. |Downloads| image:: https://pypip.in/download/pymal/badge.svg
.. _Downloads: https://pypi.python.org/pypi/pymal/
.. |LatestVersion| image:: https://pypip.in/version/pymal/badge.svg
.. _LatestVersion: https://pypi.python.org/pypi/pymal/
.. |License| image:: https://pypip.in/license/pymal/badge.svg
.. _License: https://pypi.python.org/pypi/pymal/

Contents:

.. toctree::
   :maxdepth: 2

   objects/index

The idea
--------

Provides programmatic access to MyAnimeList data with python.
Objects in pymal are lazy-loading: they won't go out and fetch MAL info until you first-request it.

Dependencies
------------

* `BeautifulSoup4`

  * `html5lib` for BeautifulSoup4 to read html pages better.

* `requests`

  * `httpcache` for requests to have cache (might be removed because no cache can be created with mal right now).

* `pillows`
  To show users' avatars and mangas/animes icon.


Installation
------------

After cloning the repository, navigate to the directory and run `python setup.py install`.

Testing
-------

To run the tests that come with MAL Client:

1. Install nose2 (A really good package for running tests - `pip install nose2`). For more data look on [nose2](https://github.com/nose-devs/nose2 "nose2").
2. Navigate to the pymal directory
3. Run `nose2` or `python -m unittest` with a lot of parameters that I don't know.

Make sure you don't spam the tests too quickly! You're likely to be IP-banned if you do this too much in too short a span of time.

[More about tests for developers for pymal.](/tests/readme.md "pymal tests readme")

Usage
-----

Most objects data can be required by not authentication mal, but all list manipulations on MAL requires authentication.

[More about pymal for application developers.](/pymal/readme.md "pymal objects readme")

Account
^^^^^^^

To connect MAL you need an Account object.

>>> from pymal.Account import Account
>>> account = Account('mal-username', 'mal-password')

Then all your mangas and animes will be like this:

>>> animelist = account.animes
>>> mangalist = account.mangas

Anime
^^^^^

Right now, give him the anime id and it will generate the most of the things.

>>> from pymal.Anime import Anime
>>> anime = Anime(1887)  # Lucky star's anime id

For all data that can be used look in the python.
To add it its need an account object to related on.

>>> my_anime = anime.add(account)
>>> assert type(my_anime) != type(anime)

After adding an anime, you will found it in your list!

>>> animelist.reload()
>>> assert my_anime in animelist

MyAnime
^^^^^^^

A class which has more attribute like the account's number of watched episodes and so on.

It has his anime under:

>>> assert my_anime.obj == anime

You can update it and delete it:

>>> my_anime.update()
>>> my_anime.delete()

Manga
^^^^^

Right now, give him the manga id and it will generate the most of the things.

>>> from pymal.Manga import Manga
>>> manga = Manga(587)  # Lucky star's manga id

All the objects under account are subclass of Anime and Manga.
To add it its need an account object to related on.

>>> my_manga = manga.add(account)
>>> assert type(my_manga) != type(manga)

After adding an manga, you will found it in your list!

>>> mangalist.reload()
>>> assert my_manga in mangalist

MyManga
^^^^^^^

A class which has more attribute like the account's number of read chapters and so on.

It has his manga under:

>>> assert my_manga.obj == manga

You can update it and delete it:

>>> my_manga.update()
>>> my_manga.delete()

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
