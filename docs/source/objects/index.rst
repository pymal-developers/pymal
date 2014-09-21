Coding
======

Contents:

.. toctree::
   :maxdepth: 2

   account
   account_objects/index
   anime
   manga
   seasons
   exceptions/index
   other

Guide lines
-----------
Some basic rules:

1. Tests are in their own directory tree that is equals to the real tree. Never put tests in here! That's why we have a folder for them :)
2. Remember that we are reading from anther server (myanimelist.net). Make everything as lazy as possible and use all the information from each data you receive.
3. Objects with same interface should inheritance from the same interface.

**Q:** Where do i put a new object?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**A:** Each object should be placed in his own file.

**Q:** Do you have any global files?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**A:** yes we do!
* `global_function.py` - Here you should find and place all the globals functions. Any function that most of other code will use and its not better any where. Some people will call it 'junk file'.
* `consts.py` - Here you should find and place all the constants of the project. More constants out here means better sharing and finding even for the test!
* `decorators.py` - Here you should find and place all the global decorators. I don't recommend to make a lot of them, only if necessary or looks better.
