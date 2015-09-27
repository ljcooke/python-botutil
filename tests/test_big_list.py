# coding: utf-8
from __future__ import unicode_literals

import os
import unittest

from botutil import BigList


SOURCE = 'tests/data/words.txt'
INDEX = SOURCE + '.index'
assert os.path.isfile(SOURCE)

DOS_SOURCE = 'tests/data/words-dos.txt'
DOS_INDEX = DOS_SOURCE + '.index'
assert os.path.isfile(DOS_SOURCE)

CSV_SOURCE = 'tests/data/oneline.csv'
CSV_INDEX = CSV_SOURCE + '.index'
assert os.path.isfile(CSV_SOURCE)


class TestStandardBigList(unittest.TestCase):

    def setUp(self):
        self.blist = BigList(SOURCE)

    def tearDown(self):
        self.blist = None

    def test_regenerate_index(self):
        old_index, new_index = None, None

        with open(INDEX, 'rb') as fp:
            old_index = fp.read()
        self.blist = None
        os.remove(INDEX)

        self.blist = BigList(SOURCE)
        if os.path.isfile(INDEX):
            with open(INDEX, 'rb') as fp:
                new_index = fp.read()

        self.assertTrue(os.path.isfile(INDEX))
        self.assertEqual(old_index, new_index)

    def test_index_size(self):
        # Expecting 5 frames: 5000 lines of input, 1024 per frame
        header_size = 20
        frame_size = 4
        file_size = os.stat(INDEX).st_size
        expected_size = header_size + (frame_size * 5)

        self.assertEqual(file_size, expected_size)

    def test_len(self):
        self.assertEqual(len(self.blist), 5000)

    def test_random_access(self):
        self.assertEqual(self.blist[0], 'page_title')
        self.assertEqual(self.blist[4000], '-sti')

    def test_negative_index(self):
        self.assertEqual(self.blist[-1], self.blist[5000 - 1])

    def test_unicode(self):
        self.assertEqual(self.blist[4970], '-λάτρης')

    def test_random_selection(self):
        self.assertTrue(self.blist.choice())

        self.assertEqual(self.blist.choice(start=0, end=0),
                         self.blist[0])
        self.assertEqual(self.blist.choice(start=-1, end=-1),
                         self.blist[-1])
        self.assertNotEqual(self.blist.choice(start=1),
                            self.blist[0])
        self.assertNotEqual(self.blist.choice(end=-2),
                            self.blist[-1])

        self.assertEqual(self.blist.random_index(start=5, end=5), 5)
        self.assertEqual(self.blist[self.blist.random_index(start=5, end=5)],
                         self.blist.choice(start=5, end=5))

        with self.assertRaises(IndexError):
            self.blist.choice(start=-1, end=0)
        with self.assertRaises(IndexError):
            self.blist.choice(start=10, end=2)

    def test_iter(self):
        num_items, num_not_empty = 0, 0
        first, last = None, None

        for item in self.blist:
            num_items += 1
            if item:
                num_not_empty += 1
            if not first:
                first = item
            last = item

        self.assertIsNotNone(first)
        self.assertIsNotNone(last)
        self.assertEqual(num_items, len(self.blist))
        self.assertEqual(num_items, num_not_empty)
        self.assertEqual(first, self.blist[0])
        self.assertEqual(last, self.blist[-1])

        for i, item in enumerate(self.blist):
            self.assertEqual(item, self.blist[i])

    def test_relatively_long_line(self):
        self.assertEqual(
            self.blist[1999], 'Lorem ipsum dolor sit amet, consectetur '
            'adipiscing elit. Aliquam ipsum lacus, molestie at consequat '
            'congue, semper id ante. Pellentesque quis augue mattis, '
            'tempor tellus id, porttitor ex. Duis a dolor vestibulum, '
            'semper lorem et, consectetur nisi. Donec in suscipit quam, '
            'tincidunt auctor libero. Nam vehicula, justo quis auctor '
            'rutrum, libero tortor pulvinar felis, et feugiat turpis '
            'turpis quis velit. Nunc maximus justo ut ipsum gravida, '
            'vel iaculis nibh sodales. Quisque euismod magna vel quam '
            'tristique, quis egestas tortor lacinia. Donec mattis luctus '
            'eros, dictum varius arcu dapibus sit amet. Aenean sem ante, '
            'lacinia sed erat at, gravida tincidunt elit. Praesent lectus '
            'risus, tincidunt ac sem sed, laoreet eleifend lorem. Fusce '
            'quis sem ut ex malesuada facilisis. Nullam auctor sit amet '
            'orci at euismod.')


class TestDosLineEndings(unittest.TestCase):

    def setUp(self):
        self.blist = BigList(DOS_SOURCE)

    def tearDown(self):
        self.blist = None

    def test_line_ending_stripped(self):
        self.assertEqual(self.blist[0], 'page_title')
        self.assertFalse(any('\r' in line for line in self.blist))


class TestCommaSeparated(unittest.TestCase):

    def setUp(self):
        self.blist = BigList(CSV_SOURCE, separator=b',')

    def tearDown(self):
        self.blist = None

    def test_len(self):
        self.assertEqual(len(self.blist), 4)


class TestInvalidInitParams(unittest.TestCase):

    def test_filename(self):
        with self.assertRaises(ValueError):
            BigList(None)
        with self.assertRaises(ValueError):
            BigList('')
        with self.assertRaises(IOError):
            BigList('invalid filename')

    def test_per_frame(self):
        with self.assertRaises(ValueError):
            BigList(SOURCE, per_frame=0)
        with self.assertRaises(ValueError):
            BigList(SOURCE, per_frame=-1)
        with self.assertRaises(ValueError):
            BigList(SOURCE, per_frame=2 ** 16)

    def test_separators(self):
        with self.assertRaises(ValueError):
            BigList(SOURCE, separator='')
        with self.assertRaises(ValueError):
            BigList(SOURCE, separator='too long')
