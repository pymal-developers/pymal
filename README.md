[![Build Status](https://travis-ci.org/tomerghelber/pymal.svg)](https://travis-ci.org/tomerghelber/pymal)
[![Coverage Status](https://coveralls.io/repos/tomerghelber/pymal/badge.png)](https://coveralls.io/r/tomerghelber/pymal)
[![Downloads](https://pypip.in/download/pymal/badge.svg)](https://pypi.python.org/pypi/pymal/)
[![Latest Version](https://pypip.in/version/pymal/badge.svg)](https://pypi.python.org/pypi/pymal/)
[![Supported Python versions](https://pypip.in/py_versions/pymal/badge.svg)](https://pypi.python.org/pypi/pymal/)
[![Supported Python implementations](https://pypip.in/implementation/pymal/badge.svg)](https://pypi.python.org/pypi/pymal/)
[![Development Status](https://pypip.in/status/pymal/badge.svg)](https://pypi.python.org/pypi/pymal/)
[![License](https://pypip.in/license/pymal/badge.svg)](https://pypi.python.org/pypi/pymal/)

pymal
==========
Provides programmatic access to MyAnimeList data with python.
Objects in pymal are lazy-loading: they won't go out and fetch MAL info until you first-request it.

Dependencies
===========
* `python`
Wasn't tried on other python 3, but i believe it will work on all types of python 3.
Won't work on python 2 (known problem is the headers of functions).
I don't believe it should be even discussed. (python 2 was announced as deprecated).
    * `3.2`
    * `3.3`
    * `3.4`
    * `pypi3`
* `BeautifulSoup4`
    * `html5lib` for BeautifulSoup4 to read html pages better.
* `requests`
    * `httpcache` for requests to have cache (might be removed because no cache can be created with mal right now).
* pillows
To show users' avatars and mangas/animes icon.

Installation
============
After cloning the repository, navigate to the directory and run `python setup.py install`.

Testing
=======
To run the tests that come with MAL Client:
1. Install nose2 (A really good package for running tests - `pip install nose2`). For more data look on [nose2](https://github.com/nose-devs/nose2 "nose2").
  If you decided to install nose 2, I recommend on the plugin nose2-cov for code statistics - `pip install nose2-cov`.
2. Navigate to the pymal directory
3. Run `nose2` or `python -m unittest` with a lot of parameters that I don't know.

Make sure you don't spam the tests too quickly! You're likely to be IP-banned if you do this too much in too short a span of time.

[More about tests for developers for pymal.](/tests/readme.md "pymal tests readme")

Usage
=====
Most objects data can be required by not authentication mal, but all list manipulations on MAL requires authentication.

[More about pymal for application developers.](/pymal/readme.md "pymal objects readme")

Account
------
To connect MAL you need an Account object.

``` python
from pymal.Account import Account
account = Account('mal-username', 'mal-password')
```

Then all your mangas and animes will be like this:

``` python
animelist = account.animes
mangalist = account.mangas
```

Anime
-----
Right now, give him the anime id and it will generate the most of the things.

``` python
from pymal.Anime import Anime
anime = Anime(1887)  # Lucky star's anime id
```

For all data that can be used look in the python.
To add it its need an account object to related on.

``` python
my_anime = anime.add(account)
assert type(my_anime) != type(anime)
```

After adding an anime, you will found it in your list!

``` python
animelist.reload()
assert my_anime in animelist
```

MyAnime
-------
A class which has more attribute like the account's number of watched episodes and so on.

It has his anime under:
``` python
assert my_anime.obj == anime
```

You can update it and delete it:
``` python
my_anime.update()
my_anime.delete()
```

Manga
-----
Right now, give him the manga id and it will generate the most of the things.

``` python
from pymal.Manga import Manga
manga = Manga(587)  # Lucky star's manga id
```

All the objects under account are subclass of Anime and Manga.
To add it its need an account object to related on.

``` python
my_manga = manga.add(account)
assert type(my_manga) != type(manga)
```

After adding an manga, you will found it in your list!

``` python
mangalist.reload()
assert my_manga in mangalist
```

MyManga
-------
A class which has more attribute like the account's number of read chapters and so on.

It has his manga under:
``` python
assert my_manga.obj == manga
```

You can update it and delete it:
``` python
my_manga.update()
my_manga.delete()
```