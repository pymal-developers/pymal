def load(function):
    """a decorator"""
    def _load_wrapper(self, *args):
        if not self._is_loaded:
            self.reload()
        return function(self, *args)
    return _load_wrapper


def my_load(function):
    """a decorator"""
    def _my_load_wrapper(self, *args):
        if not self._is_my_loaded:
            self.my_reload()
        return function(self, *args)
    return _my_load_wrapper