Testing
=======
If you read this that mean that you want to do something with the code (read or add).
This README will try to explain how all the tests are organized and how it should look like.

Running
-------
To run the tests that come with pyMAL:

1. Install nose (A package for running tests - `pip install nose`).
2. Navigate to the pymal directory
3. Run `nosetests`.

Make sure you don't spam the tests too quickly! You're likely to be IP-banned if you do this too much in too short a span of time.

Guide lines
-----------
* we are using the basic unittest that python gives us.
  Please don't add anything else like pytest and his friends. If it is really needed ask.
* For every file in pymal should be a test (if it's look smart to check it).
* Every object needs to be tested with all his function.
* Tests the returned types, with mocks and with connection to MAL.
* Any thing that it's constant should be place in `constants_for_testing.py`.
* Make assert informative by code or by message.
