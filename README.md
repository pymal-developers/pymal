Table of contents
=================
[TOC]

pymal
==========
Provides programmatic access to MyAnimeList data with python.
Objects in pymal are lazy-loading: they won't go out and fetch MAL info until you first-request it.

![Tests status on codeship](https://codeship.io/projects/57c82b50-cd5c-0131-5e65-7a624b040fbd/status "Tests status on codeship")

Dependencies
===========
* python 3.4.*
    - Wasn't tried on other python 3, but i believe it will work on all python 3.
    - Won't work on python 2 (known problem is the headers of functions). I don't believe it should be even discussed. (python 2 was announced as deprecated).
* BeautifulSoup4
    - html5lib for BeautifulSoup4 to read html pages better.
* requests
    - httpcache for requests to have cache (might be removed because no cache can be created with mal right now).

Installation
============
After cloning the repository, navigate to the directory and run `python setup.py install`.

Testing
=======
To run the tests that come with MAL Client:
1. Install nose2 (A really good package for running tests - `pip install nose2`). For more data look on [nose2](https://github.com/nose-devs/nose2 "nose2").
  If you decided to install nose 2, i recommend on the plugin nose2-cov for code statistics - `pip install nose2-cov`.
2. Navigate to the python-mal directory
3. Create a text file named account_settings.json and put your MAL username and password in dict under 'password' and 'username'.
4. Run `nose2` or `python -m unittest` with a lot of parameters that i don't know.

Make sure you don't spam the tests too quickly! You're likely to be IP-banned if you do this too much in too short a span of time.

    ----------- coverage: platform win32, python 3.4.1-final-0 -----------
    Name                          Stmts       Miss     Branch    BrMiss            Cover
    ------------------------------------------------------------------------------------
    pymal\Account               110/81       29/18      18/10      8/7     71.09%/72.53%
    pymal\AccountAnimes         125/123      42/10      28/24     16/8     62.09%/87.76%
    pymal\AccountMangas         125/123      42/10      28/24     16/8     62.09%/87.76%
    pymal\Anime                 273/232      59/8       57/49     23/14    75.15%/92.17%
    pymal\Manga                 272/235      53/11      59/51     24/14    76.74%/91.26%
    pymal\MyAnime               226/231      28/21      38/40     17/14    82.95%/87.08%
    pymal\MyManga               228/223      27/26      42/44     15/17    84.44%/84.48%
    pymal\Season                 43/39       12/12       2/2       0/1     73.33%/68.29%
    pymal\Seasons                57/57       28/22      10/10      4/4     52.24%/61.19%
    pymal\global_functions       92/80       20/11      32/28      9/7     76.61%/83.33%
    ------------------------------------------------------------------------------------
    TOTAL                     1551/1434    340/149    314/282    132/94    74.69%/85.84%
    Name                     Stmts   Miss Branch BrMiss     Cover

    (new/old)

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
my_anime = anime.add_anime(account)
assert type(my_anime) != type(anime)
assert issubclass(my_anime.__class__, anime.__class__)
```

MyAnime
-------
A subclass of Anime which has more attribute like the account's number of watched episodes and so on.

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
my_manga = manga.add_anime(account)
assert type(my_manga) != type(manga)
assert issubclass(my_manga.__class__, manga.__class__)
```

MyManga
-------
A subclass of Manga which has more attribute like the account's number of read chapters and so on.