import os

# pip install twitter
import twitter


def post_tweet(text):
    if len(text) > 140:
        raise ValueError('tweet is too long')
    auth = twitter.OAuth(os.environ['TWITTER_USER_TOKEN'],
                         os.environ['TWITTER_USER_SECRET'],
                         os.environ['TWITTER_CONSUMER_KEY'],
                         os.environ['TWITTER_CONSUMER_SECRET'])
    t = twitter.Twitter(auth=auth)
    return t.statuses.update(status=text, trim_user=True)
