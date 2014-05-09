[TOC]

# MAL Client

Provides programmatic access to MyAnimeList data with python.

# Dependencies

* python 3.4.*
* BeautifulSoup
* requests

# Installation

After cloning the repository, navigate to the directory and run `python setup.py install`.

# Usage
Pretty much everything on MAL requires authentication, so you'll want to do that first

```!#python
from myanimelist.Account import Account
account = Account('mal-username', 'mal-password')
```

Then if you want to fetch an anime, say:

```!#python
anime = account.animes[1]
print(anime)
```

Objects in MAL Clinet are lazy-loading: they won't go out and fetch MAL info until you first-request it. So here, if you want to retrieve all your anime title:

```!#python
for anime in account.animes:
    print(anime.title)
```

You'll note that there's a pause while anime's information is fetched from MAL.

# Testing

To run the tests that come with MAL Client:

1. Navigate to the python-mal directory
2. Create a textfile named credentials.txt and put your MAL username and password in it, and user user agent.
3. Run `python -m unittest`.

Make sure you don't spam the tests too quickly! You're likely to be IP-banned if you do this too much in too short a span of time.