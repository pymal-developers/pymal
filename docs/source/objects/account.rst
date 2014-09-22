Account
=======
It should held all the data about the account.
Also it's the only one who has the password and authenticated connection. All other object should use him.
Objects which connected to Account are placed under `account_object` folder.

You can find there:

* :class:`account_objects.account_animes.AccountAnimes`
* :class:`account_objects.account_mangas.AccountMangas`
* :class:`account_objects.account_friends.AccountFriends`
* :class:`account_objects.my_anime.MyAnime`
* :class:`account_objects.my_manga.MyManga`

.. automodule:: account
    :members:
