import os

import tweepy


def get_replies(max_results=100):
    client = tweepy.Client(bearer_token=os.getenv('TWITTER_BEARER_TOKEN'))

    tweets = client.search_recent_tweets(
        # query='(@CryptoBugsx2B67 -"to get rule" is:retweet) OR (-"to get rule" to:CryptoBugsx2B67)',
        # query='retweets_of:CryptoBugsx2B67',
        query='@CryptoBugsx2B67 -"to get rule" -"dm for promotion" -"promote it on" -"get dodge rewards"  ',
        max_results=max_results,
        user_fields=['public_metrics'],
        expansions=['author_id', 'in_reply_to_user_id', 'entities.mentions.username'],
        tweet_fields=['created_at', 'referenced_tweets'],

    )

    return tweets


replies = get_replies()

print(replies)
