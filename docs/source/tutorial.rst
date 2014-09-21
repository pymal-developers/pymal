Tutorial
========

Installation
------------

If you want to checkout a repository, navigate to the directory and run `python setup.py install`.
The recommended way is to run `pip install pymal`.

Usage
-----
Most objects data can be required by not authentication mal, but all list manipulations on MAL requires authentication.

:class:`account.Account`
^^^^^^^^^^^^^^^^^^^^^^^^
To connect MAL you need an :class:`account.Account` object.

>>> from pymal.account import Account
>>> account = Account('mal-username', 'mal-password')

Then all your mangas and animes will be like this:

>>> animelist = account.animes
>>> mangalist = account.mangas

:class:`anime.Anime`
^^^^^^^^^^^^^^^^^^^^
Right now, give him the anime id and it will generate the most of the things.

>>> from pymal.anime import Anime
>>> anime = Anime(1887)  # Lucky star's anime id

For all data that can be used look in the python.
To add it its need an :class:`account.Account` object to related on.

>>> my_anime = anime.add(account)
>>> assert type(my_anime) != type(anime)

After adding an :class:`anime.Anime`, you will found it in your list!

>>> assert my_anime not in animelist
>>> animelist.reload()
>>> assert my_anime in animelist

:class:`account_objects.my_anime.MyAnime`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
A class which has more attribute like the account's number of watched episodes and so on.

It has his :class:`anime.Anime` under:

>>> assert my_anime.obj == anime

You can update it and delete it:

>>> my_anime.update()
>>> my_anime.delete()

:class:`manga.Manga`
^^^^^^^^^^^^^^^^^^^^
Right now, give him the :class:`manga.Manga` id and it will generate the most of the things.

>>> from pymal.manga import Manga
>>> manga = Manga(587)  # Lucky star's manga id

All the objects under :class:`account.Account` are subclass of :class:`anime.Anime` and :class:`manga.Manga`.
To add it its need an :class:`account.Account` object to related on.

>>> my_manga = manga.add(account)
>>> assert type(my_manga) != type(manga)

After adding an :class:`manga.Manga`, you will found it in your list!

>>> assert my_manga not in mangalist
>>> mangalist.reload()
>>> assert my_manga in mangalist

:class:`account_objects.my_manga.MyManga`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
A class which has more attribute like the account's number of read chapters and so on.

It has his :class:`manga.Manga` under:

>>> assert my_manga.obj == manga

You can update it and delete it:

>>> my_manga.update()
>>> my_manga.delete()
