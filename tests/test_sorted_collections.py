import unittest
from operator import itemgetter

from src import sorted_collection


class TestSortedCollection(unittest.TestCase):
    def setUp(self):
        self.records = [
            ("a", "foo", 30),
            ("b", "bar", 28),
            ("c", "baz", 22),
            ("d", "hogehoge", 32),
        ]
        self.key = itemgetter(2)
        self.target = sorted_collection.SortedCollection(self.records, self.key)

    def test_constructor(self):
        sorted_records = [
            ("c", "baz", 22),
            ("b", "bar", 28),
            ("a", "foo", 30),
            ("d", "hogehoge", 32),
        ]
        self.assertEqual(self.target.key, self.key)
        self.assertListEqual(self.target.items, sorted_records)
        self.assertListEqual(self.target._keys, [22, 28, 30, 32])

    def test_key_setter(self):
        self.target.key = itemgetter(0)
        new_sorted_records = [
            ("a", "foo", 30),
            ("b", "bar", 28),
            ("c", "baz", 22),
            ("d", "hogehoge", 32),
        ]
        self.assertListEqual(self.target.keys, ["a", "b", "c", "d"])
        self.assertListEqual(self.target.items, new_sorted_records)

    def test_clear(self):
        self.target.clear()
        self.assertEqual(self.target._items, [])

    def test_copy(self):
        copy = self.target.copy()
        self.assertEqual(self.target.items, copy.items)

    def test_len(self):
        self.assertEqual(len(self.target), 4)

    def test_getitem(self):
        self.assertEqual(self.target[0], self.target.items[0])
        self.assertEqual(self.target[1], self.target.items[1])
        self.assertEqual(self.target[2], self.target.items[2])
        self.assertEqual(self.target[3], self.target.items[3])

    def test_iter(self):
        for it, item in zip(self.target, self.target.items):
            self.assertEqual(it, item)

    def test_reversed(self):
        for it, item in zip(reversed(self.target), reversed(self.target.items)):
            self.assertEqual(it, item)

    def test_contains(self):
        self.assertTrue(self.records[0] in self.target)
        self.assertTrue(self.records[1] in self.target)
        self.assertTrue(self.records[2] in self.target)
        self.assertTrue(self.records[3] in self.target)
        self.assertFalse(("e", "foo", 30) in self.target)

    def test_index(self):
        self.assertEqual(self.target.index(22), 0)
        self.assertEqual(self.target.index(28), 1)
        self.assertEqual(self.target.index(30), 2)
        self.assertEqual(self.target.index(32), 3)
        not_exist_keys = [0, 11, 23, 31]
        for not_exist_key in not_exist_keys:
            with self.assertRaises(ValueError):
                self.target.index(not_exist_key)

    def test_count(self):
        records = [
            ("foo", 1),
            ("bar", 1),
            ("baz", 2),
            ("hoge", 3),
            ("hogehoge", 3),
            ("hogehogehoge", 3),
        ]
        s = sorted_collection.SortedCollection(records, itemgetter(1))
        self.assertEqual(s.count(1), 2)
        self.assertEqual(s.count(2), 1)
        self.assertEqual(s.count(3), 3)

    def test_insert(self):
        # original keys was 22 28 30 32
        # new keys would be 22 22 28 30 31 32
        new_record1 = ("e", "fuga", 31)
        new_record2 = ("f", "fugafuga", 22)
        self.target.insert(new_record1)
        self.target.insert(new_record2)
        self.assertSequenceEqual(self.target.items[4], new_record1)
        self.assertSequenceEqual(self.target.items[0], new_record2)

    def test_insert_right(self):
        # original keys was 22 28 30 32
        # new keys would be 22 22 28 30 31 32
        new_record1 = ("e", "fuga", 31)
        new_record2 = ("f", "fugafuga", 22)
        self.target.insert_right(new_record1)
        self.target.insert_right(new_record2)
        self.assertSequenceEqual(self.target.items[4], new_record1)
        self.assertSequenceEqual(self.target.items[1], new_record2)

    def test_remove(self):
        new_records = [("a", "foo", 30), ("d", "hogehoge", 32)]
        self.target.remove(22)
        self.target.remove(28)
        self.assertSequenceEqual(self.target.keys, (30, 32))
        self.assertSequenceEqual(self.target.items, new_records)

    def test_find(self):
        records = [
            ("c", "baz", 22),
            ("b", "bar", 28),
            ("a", "foo", 30),
            ("d", "hogehoge", 32),
        ]
        test_cases = [
            ("==", 22, records[0]),
            ("==", 28, records[1]),
            (">", 21, records[0]),
            (">", 22, records[1]),
            (">=", 21, records[0]),
            (">=", 22, records[0]),
            ("<", 31, records[2]),
            ("<", 32, records[2]),
            ("<=", 31, records[2]),
            ("<=", 32, records[3]),
        ]
        for relation_op, key, expected in test_cases:
            with self.subTest(relation_op=relation_op, key=key, expected=expected):
                self.assertEqual(self.target.find(relation_op, key), expected)

    def test_find_raises(self):
        records = [
            ("c", "baz", 22),
            ("b", "bar", 28),
            ("a", "foo", 30),
            ("d", "hogehoge", 32),
        ]
        invalid_cases = [
            ("==", 21),
            ("==", 27),
            (">", 41),
            (">", 32),
            (">=", 33),
            (">=", 52),
            ("<", 21),
            ("<", 22),
            ("<=", 21),
            ("<=", 20),
        ]
        for relation_op, key in invalid_cases:
            with self.assertRaises(ValueError):
                self.target.find(relation_op, key)
