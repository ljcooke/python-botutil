BigList index file format
=========================

Integer types
-------------

Integers are encoded in little-endian order. All integers are unsigned.

<table>
  <tr>
    <th>Bytes</th>
    <th>Bits</th>
    <th>Python struct format</th>
  </tr>
  <tr>
    <th>1</th>
    <td>8</td>
    <td><code>B</code></th>
  </tr>
  <tr>
    <th>2</th>
    <td>16</td>
    <td><code>&lt;H</code></th>
  </tr>
  <tr>
    <th>4</th>
    <td>32</td>
    <td><code>&lt;L</code></th>
  </tr>
  <tr>
    <th>8</th>
    <td>64</td>
    <td><code>&lt;Q</code></th>
  </tr>
</table>

File layout
-----------

  * <i>Header</i> (20 bytes)

      * Magic number (8 bytes)

          * ASCII string <code>BigList</code> (7 bytes)

          * Version number (1-byte int)

      * Number of lines per frame (2-byte int)

          > Default: 1,024 (<code>00 04</code>)

      * Total number of lines (8-byte int)

      * Separator character (1 byte)

          > Default: ASCII newline (<code>0A</code>)

      * Padding (1 byte)

  * 0 or more <i>Frame</i> objects (4 bytes each)

Frame
-----

A frame consists of a single field:

  * Number of bytes (4-byte int)

    This indicates how many bytes in the source file are represented by this
    frame.
