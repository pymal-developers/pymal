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
    pymal\Account              101/110      24/29      18/18       7/8     73.95%/71.09%
    pymal\AccountAnimes        122/125      38/42      28/28      16/16    64.00%/62.09%
    pymal\AccountMangas        122/125      38/42      28/28      16/16    64.00%/62.09%
    pymal\Anime                271/273      54/59      57/57      23/23    76.52%/75.15%
    pymal\Manga                270/272      48/53      59/59      24/24    78.12%/76.74%
    pymal\MyAnime              224/226      24/28      38/38      17/17    84.35%/82.95%
    pymal\MyManga              226/228      23/27      42/42      15/15    85.82%/84.44%
    pymal\Season                40/43        8/12       2/2        0/1     80.95%/73.33%
    pymal\Seasons               54/57       24/28      10/10       4/4     56.25%/52.24%
    pymal\global_functions      88/92       16/20      32/22       9/9     79.17%/76.61%
    ------------------------------------------------------------------------------------
    TOTAL                     1518/1551    297/340    314/282    132/94    76.64%/74.69%
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
