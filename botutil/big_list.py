"""
Big list

This class provides random access to lines of text in a file.

It is intended for files with a very large number of short lines. It provides
fast, random access to lines without reading the entire file into memory.

To make this work, it generates a small index file alongside the original file.
This is generated behind the scenes the first time the file is read, and
whenever the original file is modified.

Usage example:

    blist = BigList('lines.txt')

    print('Total lines:', len(blist))
    print('First line:', blist[0])
    print('Last line:', blist[-1])

"""
import logging
import os
import random
import struct
from collections import namedtuple


MAGIC_NUMBER = b'BigList\x01'

DEFAULT_LINES_PER_FRAME = 1024
DEFAULT_SEPARATOR = b'\n'


Frame = namedtuple('Frame', ['offset', 'num_bytes'])


class BigListOutdatedException(Exception):
    """
    Exception raised when the index file must be regenerated.

    """
    pass


class BigList:
    """
    Object for providing random access to lines in a file.

    """
    def __init__(self, filename,
                 encoding='utf-8',
                 per_frame=DEFAULT_LINES_PER_FRAME,
                 separator=DEFAULT_SEPARATOR):
        """
        Create a new object to read lines from a file. Will generate a separate
        index file alongside the original file.

        Lines are read as UTF-8 strings. An alternative encoding may be
        specified. To receive bytes instead of strings, set None as the
        encoding.

        The per_frame parameter determines the number of lines which may be
        read into memory when retrieving a line. Smaller values will result in
        a larger index file; larger values will use more memory.

        Lines are separated by an ASCII newline character. A different
        separator may be specified, though it must be a single byte.

        The following exceptions may be raised:

          - ValueError for invalid input
          - IOError if the source file does not exist
          - BigListOutdatedException if there is a problem with parsing the
            index file after generating it.

        """
        if not filename:
            raise ValueError('filename is required')
        if not os.path.isfile(filename):
            raise IOError('file not found: {}'.format(repr(filename)))
        if not isinstance(separator, bytes) or len(separator) != 1:
            raise ValueError('separator must be a single byte')
        if not 0 < per_frame < 2 ** 16:
            raise ValueError('per_frame must be a 16-bit unsigned integer > 0')

        self._filename = filename
        self._encoding = encoding
        self._separator = separator
        self._index_filename = self.filename + '.index'
        self._per_frame = per_frame
        self._num_lines = 0
        self._frames = []
        self._active_frame_index = None
        self._active_frame_lines = None

        generate = True
        if self._index_exists():
            try:
                logging.debug('Reading existing index')
                self._read_index()
                generate = False
            except BigListOutdatedException:
                logging.debug('Index out of date')
                pass
        if generate:
            logging.debug('Generating index')
            self._generate_index()
            logging.debug('Reading new index')
            self._read_index()

    def __repr__(self):
        return '<{} filename={} lines={}>'.format(
            self.__class__.__name__, repr(self._filename), self._num_lines)

    def __len__(self):
        return self._num_lines

    def __getitem__(self, line_index):
        if line_index < 0:
            line_index += self._num_lines
        if not (0 <= line_index < self._num_lines):
            raise IndexError('list index out of range')

        frame_index, index_in_frame = divmod(line_index, self._per_frame)
        lines = self._read_frame_lines(frame_index)
        item = lines[index_in_frame]

        encoding = self._encoding
        return item.decode(encoding) if encoding else item

    @property
    def filename(self):
        return self._filename

    def choice(self, start=0, end=-1):
        """
        Return a random string from the list.

        """
        index = self.random_index(start, end)
        return self[index]

    def random_index(self, start=0, end=-1):
        """
        Return a random index.

        """
        count = len(self)
        if not count:
            raise IndexError('no items to choose from')
        if start < 0:
            start += count
        if end < 0:
            end += count

        diff = end - start + 1
        if diff < 0:
            raise IndexError('start is greater than end')

        return random.randint(start, end)

    def _read_frame_lines(self, frame_index):
        sep = self._separator

        if self._active_frame_index != frame_index:
            frame = self._frames[frame_index]

            with open(self._filename, 'rb') as fp:
                fp.seek(frame.offset)
                frame_bytes = fp.read(frame.num_bytes)
                assert len(frame_bytes) == frame.num_bytes

                if frame_bytes.endswith(sep):
                    frame_bytes = frame_bytes[:-1]

                lines = frame_bytes.split(sep)
                logging.debug('Read {} line(s) for frame {}'
                              .format(len(lines), frame_index))

                self._active_frame_index = frame_index
                self._active_frame_lines = lines

        return self._active_frame_lines

    def _index_exists(self):
        """
        Check whether the index file is outdated without reading it.

        """
        if not os.path.isfile(self._index_filename):
            return False

        file_stat = os.stat(self._filename)
        index_stat = os.stat(self._index_filename)
        return file_stat.st_mtime < index_stat.st_mtime

    def _generate_index(self):
        """
        Read the source file and generate an index file.

        """
        sep = self._separator
        per_frame = self._per_frame
        total_lines = 0
        frames = []
        frame_offset, frame_lines = 0, 0

        with open(self._filename, 'rb') as fp:

            def pack_frame():
                end = fp.tell()
                num_bytes = end - frame_offset
                assert 0 <= num_bytes < 2**32
                if num_bytes > 0:
                    return end, struct.pack('<L', num_bytes)
                else:
                    return end, None

            last_char = ''

            while True:
                char = fp.read(1)
                if not char:
                    break
                last_char = char

                if char == sep:
                    frame_lines += 1
                    assert 1 <= frame_lines <= per_frame

                    if frame_lines == per_frame:
                        next_offset, frame = pack_frame()
                        if frame:
                            frames.append(frame)
                            total_lines += frame_lines
                        frame_offset, frame_lines = next_offset, 0

            _, frame = pack_frame()
            if frame:
                frames.append(frame)
                total_lines += frame_lines + (0 if last_char == sep else 1)

        header = MAGIC_NUMBER + struct.pack(
            '<HQcx', per_frame, total_lines, sep)
        assert len(header) == 20

        with open(self._index_filename, 'wb') as fp:
            fp.write(header)
            fp.write(b''.join(frames))

    def _read_index(self):
        """
        Read information from the index file.

        Will raise BigListOutdatedException if the index file must be
        regenerated.

        """
        with open(self._index_filename, 'rb') as fp:
            magic = fp.read(8)
            logging.debug('Magic number = {}'.format(repr(magic)))
            if magic != MAGIC_NUMBER:
                raise BigListOutdatedException

            header_bytes = fp.read(12)
            if len(header_bytes) != 12:
                raise BigListOutdatedException
            per_frame, num_lines, sep = struct.unpack('<HQcx', header_bytes)
            logging.debug('Lines per frame = {}'.format(per_frame))
            logging.debug('Total lines = {}'.format(num_lines))
            logging.debug('Separator = {}'.format(repr(sep)))

            if per_frame != self._per_frame or sep != self._separator:
                raise BigListOutdatedException

            num_frames, last_frame_lines = divmod(num_lines, per_frame)
            if last_frame_lines:
                num_frames += 1
            logging.debug('Total frames = {}'.format(num_frames))

            frames, offset = [], 0
            for i in range(num_frames):
                frame_bytes = fp.read(4)
                if len(frame_bytes) != 4:
                    raise BigListOutdatedException

                num_bytes = struct.unpack('<L', frame_bytes)[0]
                frame = Frame(offset=offset, num_bytes=num_bytes)
                frames.append(frame)

                offset += num_bytes

            self._num_lines = num_lines
            self._frames = frames
            self._active_frame = None

            eof = not fp.read(1)
            logging.debug('Reached EOF in index = {}'.format(eof))
