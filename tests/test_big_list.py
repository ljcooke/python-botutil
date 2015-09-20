import os
import unittest

from botutil import BigList

SOURCE = 'tests/data/words.txt'
INDEX = 'tests/data/words.txt.index'

assert os.path.isfile(SOURCE)
assert os.path.isfile(INDEX)

class TestBigList(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()
