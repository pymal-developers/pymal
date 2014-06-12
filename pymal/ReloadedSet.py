__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

import collections

from pymal import decorators


class ReloadedSet(collections.Set):
    @property
    def _values(self):
        raise NotImplemented()

    def reload(self):
        raise NotImplemented()

    def __contains__(self, item):
        return item in self._values

    def __iter__(self):
        return iter(self._values)

    def __len__(self):
        return len(self._values)

    def issubset(self, other):
        return self <= frozenset(other)

    def issuperset(self, other):
        return self >= frozenset(other)

    def union(self, *others):
        res = set(self)
        for other in others:
            res |= frozenset(other)
        return res

    def __or__(self, other):
        return self.union(other)

    def intersection(self, *others):
        res = set(self)
        for other in others:
            res &= frozenset(other)
        return res

    def __and__(self, other):
        return self.intersection(other)

    def difference(self, *others):
        res = set(self)
        for other in others:
            res -= frozenset(other)
        return res

    def __sub__(self, other):
        return self.difference(other)

    def symmetric_difference(self, other):
        return set(self) ^ frozenset(other)

    def __xor__(self, other):
        return self.symmetric_difference(other)

class ReloadedSetSingletonFactoryType(type(ReloadedSet), decorators.SingletonFactory):
    pass


class ReloadedSetSingletonFactory(ReloadedSet, metaclass=ReloadedSetSingletonFactoryType):
    pass