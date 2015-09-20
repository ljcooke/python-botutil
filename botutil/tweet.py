import os

# pip install twitter
import twitter


def post_tweet(text, user_token=None, user_secret=None,
               consumer_key=None, consumer_secret=None):

    if len(text) > 140:
        raise ValueError('tweet is too long')

    auth = twitter.OAuth(
        user_token or os.environ['TWITTER_USER_TOKEN'],
        user_secret or os.environ['TWITTER_USER_SECRET'],
        consumer_key or os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret or os.environ['TWITTER_CONSUMER_SECRET'])

    t = twitter.Twitter(auth=auth)
    return t.statuses.update(status=text, trim_user=True)
