Objects
=================================

Contents:

.. toctree::
   :maxdepth: 2

   account
   account_objects/index
   anime
   manga
   seasons
   exceptions/index

Usage
=====

Most objects data can be required by not authentication mal, but all list manipulations on MAL requires authentication.

[More about pymal for application developers.](/pymal/readme.md "pymal objects readme")

Account
-------

To connect MAL you need an Account object.

>>> from pymal.Account import Account
>>> account = Account('mal-username', 'mal-password')

Then all your mangas and animes will be like this:

>>> animelist = account.animes
>>> mangalist = account.mangas

Anime
-----

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
-------

A class which has more attribute like the account's number of watched episodes and so on.

It has his anime under:

>>> assert my_anime.obj == anime

You can update it and delete it:

>>> my_anime.update()
>>> my_anime.delete()

Manga
-----

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
-------

A class which has more attribute like the account's number of read chapters and so on.

It has his manga under:

>>> assert my_manga.obj == manga

You can update it and delete it:

>>> my_manga.update()
>>> my_manga.delete()
