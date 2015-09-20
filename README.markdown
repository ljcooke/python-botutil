botutil
=======

Small libraries for Python 3 botmakers.

The [twitter][pypi-twitter] package is required. Install with:

    pip3 install twitter


Twitter
-------

### botutil.post_tweet()

Tweet a string and receive the Twitter response.

By default it reads Twitter credentials from the environment variables. This
allows you to keep API tokens out of the code. For example, you might run the
following in the shell before running a bot script:

    export TWITTER_CONSUMER_KEY="appkey"
    export TWITTER_CONSUMER_SECRET="appsecret"
    export TWITTER_USER_TOKEN="123456789-mytoken"
    export TWITTER_USER_SECRET="mysecret"


File access
-----------

### botutil.BigList

This class provides fast random access to lines of text in a file.

It's useful for dealing with a large number of small lines – for example,
[@everywikt][everywikt] reads from a list of over 4&nbsp;million words, one
per line.

### botutil.DB

A wrapper class for working with SQLite databases.
It disables autocommit by default.



[everywikt]: https://twitter.com/everywikt
[pypi-twitter]: https://pypi.python.org/pypi/twitter
