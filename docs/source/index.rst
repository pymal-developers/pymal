.. pymal documentation master file, created by
   sphinx-quickstart on Fri Sep 19 13:23:51 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pymal's documentation!
=================================

|DevelopmentStatus|_ |SupportedPythonversions|_ |SupportedPythonimplementations|_

|Downloads|_ |LatestVersion|_ |License|_

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

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
