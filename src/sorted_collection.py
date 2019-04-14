from bisect import bisect_left, bisect_right
from collections.abc import Collection
from typing import Any, Callable, Iterable, Sequence


class SortedCollection(Collection):
    def __init__(self, items: Iterable, key: Callable[[Sequence], Any]):
        self._key = key
        self._items = sorted(items, key=key)
        self._keys = [key(item) for item in self._items]

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        if key is not self.key:
            self.__init__(self.items, key=key)

    @property
    def items(self):
        return self._items

    @property
    def keys(self):
        return self._keys

    def clear(self):
        self.__init__([], self.key)

    def copy(self):
        return self.__class__(self, self.key)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, i):
        return self.items[i]

    def __iter__(self):
        return iter(self.items)

    def __reversed__(self):
        return reversed(self.items)

    def __repr__(self):
        return "%s(%r, key=%s)" % (
            self.__class__.__name__,
            self.items,
            getattr(self.key, "__name__", repr(self.key)),
        )

    def __contains__(self, item):
        k = self.key(item)
        i = bisect_left(self.keys, k)
        j = bisect_right(self.keys, k)
        return item in self.items[i:j]

    def index(self, k):
        "Find the position of an item.  Raise ValueError if not found."
        i = bisect_left(self.keys, k)
        j = bisect_right(self.keys, k)
        return self.keys[i:j].index(k) + i

    def count(self, k):
        "Return number of occurrences of item"
        i = bisect_left(self.keys, k)
        j = bisect_right(self.keys, k)
        return self.keys[i:j].count(k)

    def insert(self, item):
        "Insert a new item.  If equal keys are found, add to the left"
        k = self.key(item)
        i = bisect_left(self.keys, k)
        self.keys.insert(i, k)
        self.items.insert(i, item)

    def insert_right(self, item):
        "Insert a new item.  If equal keys are found, add to the right"
        k = self.key(item)
        i = bisect_right(self.keys, k)
        self.keys.insert(i, k)
        self.items.insert(i, item)

    def remove(self, k):
        "Remove first occurence of item.  Raise ValueError if not found"
        i = self.index(k)
        del self.keys[i]
        del self.items[i]

    def find(self, relation_op, k):
        find_func_dict = {
            "==": self._find_eq,
            ">": self._find_gt,
            ">=": self._find_ge,
            "<": self._find_lt,
            "<=": self._find_le,
        }
        return find_func_dict[relation_op](k)

    def _find_eq(self, k):
        "Return first item with a key == k.  Raise ValueError if not found."
        i = bisect_left(self.keys, k)
        if i != len(self) and self.keys[i] == k:
            return self.items[i]
        raise ValueError("No item found with key equal to: %r" % (k,))

    def _find_le(self, k):
        "Return last item with a key <= k.  Raise ValueError if not found."
        i = bisect_right(self.keys, k)
        if i:
            return self._items[i - 1]
        raise ValueError("No item found with key at or below: %r" % (k,))

    def _find_lt(self, k):
        "Return last item with a key < k.  Raise ValueError if not found."
        i = bisect_left(self.keys, k)
        if i:
            return self._items[i - 1]
        raise ValueError("No item found with key below: %r" % (k,))

    def _find_ge(self, k):
        "Return first item with a key >= equal to k.  Raise ValueError if not found"
        i = bisect_left(self.keys, k)
        if i != len(self):
            return self._items[i]
        raise ValueError("No item found with key at or above: %r" % (k,))

    def _find_gt(self, k):
        "Return first item with a key > k.  Raise ValueError if not found"
        i = bisect_right(self.keys, k)
        if i != len(self):
            return self._items[i]
        raise ValueError("No item found with key above: %r" % (k,))
