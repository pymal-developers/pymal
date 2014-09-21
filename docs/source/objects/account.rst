Account
=======
It should held all the data about the account.
Also it's the only one who has the password and authenticated connection. All other object should use him.
Objects which connected to Account are placed under `account_object` folder.

You can find there:

* :class:`account_animes.AccountAnimes`
* :class:`account_mangas.AccountMangas`
* :class:`account_friends.AccountFriends`
* :class:`my_anime.MyAnime`
* :class:`my_manga.MyManga`

.. automodule:: account
.. autoclass:: Account
    :members:
