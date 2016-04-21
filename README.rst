botutil
=======

Small libraries for Python botmakers. Supports Python 3 and 2.7.

The `twitter <pypi-twitter>`_ package is required. Install it with:

.. code:: bash

  pip3 install twitter  # for Python 3
  # or
  pip install twitter   # for Python 2

Some unit tests are provided to test the libraries with both Python 3 and
Python 2.7. Run these with:

.. code:: bash

  make test
  # or
  make test_python3
  make test_python2

.. _pypi-twitter: https://pypi.python.org/pypi/twitter


Twitter
-------

botutil.post_tweet()
~~~~~~~~~~~~~~~~~~~~

Tweet a string and receive the Twitter response.

.. code:: python

  tweet = botutil.post_tweet('beep boop')

It reads Twitter credentials from environment variables. This allows you to
keep API tokens out of the code. For example, you might run the following in
the shell before running a bot script:

.. code:: bash

  export TWITTER_CONSUMER_KEY="appkey"
  export TWITTER_CONSUMER_SECRET="appsecret"
  export TWITTER_USER_TOKEN="123456789-mytoken"
  export TWITTER_USER_SECRET="mysecret"


File access
-----------

botutil.BigList
~~~~~~~~~~~~~~~

This class provides fast random access to lines of text in a file.

.. code:: python

  blist = BigList('lines.txt')

  total_lines = len(blist)
  millionth_line = blist[999999]
  last_line = blist[-1]
  random_line = blist.choice()

It's useful for dealing with a large number of small lines – for example,
`@everywikt <everywikt>`_ reads from a list of over 4&nbsp;million words, one
per line.

.. _everywikt: https://twitter.com/everywikt

botutil.DB
~~~~~~~~~~

A wrapper class for working with SQLite databases.

.. code:: python

  db = DB('corpus.sqlite3')
  c = db.cursor()

  c.execute('BEGIN')
  c.execute('UPDATE Word SET tweeted = ? WHERE id = ?', (1, 123))
  c.execute('COMMIT')

It's intended for working with explicit transactions, as shown above, so
autocommit is disabled by default.


License
-------

Copyright (c) 2015, Liam Cooke

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
