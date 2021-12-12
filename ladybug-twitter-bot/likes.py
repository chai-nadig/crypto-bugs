import os

import tweepy


def get_replies(max_results=100):
    client = tweepy.Client(bearer_token=os.getenv('TWITTER_BEARER_TOKEN'))

    tweets = client.search_recent_tweets(
        # query='(@CryptoBugsx2B67 -"to get rule" is:retweet) OR (-"to get rule" to:CryptoBugsx2B67)',
        query='retweets_of:@CryptoBugsx2B67',
        max_results=max_results,
        user_fields=['public_metrics'],
        expansions=['author_id'],
        tweet_fields=['created_at'],

    )

    return tweets


replies = get_replies()

print(replies)
