Table of contents
=================
[TOC]

pymal
==========
If you read this that mean that you want to do something with the code (read or add).
This README will try to explain how all the tests are organized and how it should look like.

Dependencies
===========
pymal global dependencies
-------------------------
* python 3.4.*
* BeautifulSoup
* requests

test dependencies
-----------------
 * we are using the basic unittest that python gives us.
    Please don't add anything else like pytest and his friends. If it is really needed ask.
 * Recommended to install nose2 (we have a config for it in the main folder and its really easy).
    With pip `pip install nose2`.
    Together with it, install the the plugin nose2-cov - `pip install nose2-cov`.
 * Of course you can use the native python unittest with `python -m unittest`.

Usage
=====
For every file in pymal should be a test (if it's look smart to check it).
Every object needs to be tested with all his function. At least to check the return type.
Any thing that it's constant should be place in `constants_for_testing.py`.
All configurable data should be read from `account_settings.json`.
Try to write informative message in assert if the assert shows nothing.