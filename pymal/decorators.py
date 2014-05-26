__authors__   = ""
__copyright__ = "(c) 2014, pymal"
__license__   = "BSD License"
__contact__   = "Name Of Current Guardian of this file <email@address>"


def load(function):
    """
    This decorator checking of the class was loaded and load it if needed.
    For lazy.
    """
    def _load_wrapper(self, *args):
        if not self._is_loaded:
            self.reload()
        return function(self, *args)
    return _load_wrapper


def my_load(function):
    """
    This decorator checking of the class was loaded and load it if needed.
    For lazy.
    Same as load but loading different function and checking different value.
    """
    def _my_load_wrapper(self, *args):
        if not self._is_my_loaded:
            self.my_reload()
        return function(self, *args)
    return _my_load_wrapper