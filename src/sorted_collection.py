from bisect import bisect_left, bisect_right
from collections.abc import Collection
from typing import Any, Callable, Iterable, Iterator, List, Sequence

ItemGetter = Callable[[Sequence], Any]


class SortedCollection(Collection):
    def __init__(self, items: Iterable, key: ItemGetter) -> None:
        self._key = key
        self._items = sorted(items, key=key)
        self._keys = [key(item) for item in self._items]

    @property
    def key(self) -> ItemGetter:
        return self._key

    @key.setter
    def key(self, key: ItemGetter) -> None:
        if key != self.key:
            self._key = key
            self._items = sorted(self.items, key=key)
            self._keys = [key(item) for item in self._items]

    @property
    def items(self) -> List:
        return self._items

    @property
    def keys(self) -> List:
        return self._keys

    def clear(self) -> None:
        self._key = self.key
        self._items = []

    def copy(self) -> "SortedCollection":
        return self.__class__(self, self.key)

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, i: int) -> Any:
        return self.items[i]

    def __iter__(self) -> Iterator:
        return iter(self.items)

    def __reversed__(self) -> Iterator:
        return reversed(self.items)

    def __repr__(self) -> str:
        return "%s(%r, key=%s)" % (
            self.__class__.__name__,
            self.items,
            getattr(self.key, "__name__", repr(self.key)),
        )

    def __contains__(self, item: Any) -> bool:
        k = self.key(item)
        i = bisect_left(self.keys, k)
        j = bisect_right(self.keys, k)
        return item in self.items[i:j]

    def index(self, k: int) -> int:
        "Find the position of an item.  Raise ValueError if not found."
        i = bisect_left(self.keys, k)
        j = bisect_right(self.keys, k)
        return self.keys[i:j].index(k) + i

    def count(self, k: int) -> int:
        "Return number of occurrences of item"
        i = bisect_left(self.keys, k)
        j = bisect_right(self.keys, k)
        return self.keys[i:j].count(k)

    def insert(self, item: Any) -> None:
        "Insert a new item.  If equal keys are found, add to the left"
        k = self.key(item)
        i = bisect_left(self.keys, k)
        self.keys.insert(i, k)
        self.items.insert(i, item)

    def insert_right(self, item: Any) -> None:
        "Insert a new item.  If equal keys are found, add to the right"
        k = self.key(item)
        i = bisect_right(self.keys, k)
        self.keys.insert(i, k)
        self.items.insert(i, item)

    def remove(self, k: int) -> None:
        "Remove first occurence of item.  Raise ValueError if not found"
        i = self.index(k)
        del self.keys[i]
        del self.items[i]

    def find(self, relation_op: str, k: int) -> Any:
        find_func_dict = {
            "==": self._find_eq,
            ">": self._find_gt,
            ">=": self._find_ge,
            "<": self._find_lt,
            "<=": self._find_le,
        }
        return find_func_dict[relation_op](k)

    def _find_eq(self, k: int) -> Any:
        "Return first item with a key == k.  Raise ValueError if not found."
        i = bisect_left(self.keys, k)
        if i != len(self) and self.keys[i] == k:
            return self.items[i]
        raise ValueError("No item found with key equal to: %r" % (k,))

    def _find_le(self, k: int) -> Any:
        "Return last item with a key <= k.  Raise ValueError if not found."
        i = bisect_right(self.keys, k)
        if i:
            return self._items[i - 1]
        raise ValueError("No item found with key at or below: %r" % (k,))

    def _find_lt(self, k: int) -> Any:
        "Return last item with a key < k.  Raise ValueError if not found."
        i = bisect_left(self.keys, k)
        if i:
            return self._items[i - 1]
        raise ValueError("No item found with key below: %r" % (k,))

    def _find_ge(self, k: int) -> Any:
        "Return first item with a key >= equal to k.  Raise ValueError if not found"
        i = bisect_left(self.keys, k)
        if i != len(self):
            return self._items[i]
        raise ValueError("No item found with key at or above: %r" % (k,))

    def _find_gt(self, k: int) -> Any:
        "Return first item with a key > k.  Raise ValueError if not found"
        i = bisect_right(self.keys, k)
        if i != len(self):
            return self._items[i]
        raise ValueError("No item found with key above: %r" % (k,))
