__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

__all__ = ['UnauthenticatedAccountError', 'MyAnimeListApiError',
           'MyAnimeListApiUpdateError', 'MyAnimeListApiDeleteError',
           'MyAnimeListApiAddError']


class UnauthenticatedAccountError(ValueError):
    pass


class MyAnimeListApiError(RuntimeError):
    pass


class MyAnimeListApiUpdateError(MyAnimeListApiError):
    pass


class MyAnimeListApiDeleteError(MyAnimeListApiError):
    pass


class MyAnimeListApiAddError(MyAnimeListApiError):
    pass


class NotASeason(ValueError):
    def __init__(self, tried_season_name):
        super().__init__("The wanted season '{0:s}' is not: 'Winter', 'Spring', 'Summer' or 'Fall'.".format(
            tried_season_name
        ))
