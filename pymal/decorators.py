__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

from reloaded_set import load


def my_load(function):
    """
    This decorator checking of the class was loaded and load it if needed.
    For lazy.
    Needs attribute _is_my_loaded and a function my_reload().
    """
    return load(flag_name='_is_my_loaded', function_name='my_reload')(function)
