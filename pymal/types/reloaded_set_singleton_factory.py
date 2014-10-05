import singleton_factory
from reloaded_set import ReloadedSet

__author__ = 'user'


class ReloadedSetSingletonFactoryType(type(ReloadedSet), singleton_factory.SingletonFactory):
    """
    A singleton factory ReloadedSet type.
    """
    pass


class ReloadedSetSingletonFactory(ReloadedSet, metaclass=ReloadedSetSingletonFactoryType):
    """
    A singleton factory ReloadedSet.
    """
    pass