import json
import os
from json import JSONDecodeError

import tweepy

from search import (
    get_tweets_by_author,
    get_tweets_by_unpopular_authors, like_tweet,
)


def main():
    max_tweet_id = get_max_tweet_id_liked()

    response = get_tweets()

    print(response.data)

    if response.data is None or len(response.data) == 0:
        print("no new recent tweets found")
        return

    max_tweet_id = max([tw.id for tw in response.data])

    save_max_tweet_id_liked(max_tweet_id)

    tweets_by_author = get_tweets_by_author(response.data)

    tweets_by_unpopular_authors = get_tweets_by_unpopular_authors(tweets_by_author, response.includes['users'])

    print("number tweets unpopular authors",
          sum([len(tweets) for author, tweets in tweets_by_unpopular_authors.items()]))

    for author_id, tweets in tweets_by_unpopular_authors.items():
        should_break = False
        for tw in tweets:
            try:
                like_tweet(tw)
                print("liked {}".format(tw.id))

            except tweepy.TooManyRequests:
                print("too many likes posted")
                should_break = True
                break

            except Exception as e:
                print("error liking tweet by unpopular author", e, author_id, tw)

        if should_break:
            break


def get_max_tweet_id_liked():
    max_tweet_id = None
    with open('./max-tweet-id-liked.json') as f:
        try:
            max_tweet_id = json.load(f)
        except JSONDecodeError:
            pass

    return max_tweet_id


def save_max_tweet_id_liked(max_tweet_id):
    with open('./max-tweet-id-liked.json', 'w') as f:
        json.dump(max_tweet_id, f, indent=4)


def get_tweets(max_results=100):
    client = tweepy.Client(bearer_token=os.getenv('TWITTER_BEARER_TOKEN'))

    return client.search_recent_tweets(
        # query='(@CryptoBugsx2B67 -"to get rule" is:retweet) OR (-"to get rule" to:CryptoBugsx2B67)',
        # query='retweets_of:CryptoBugsx2B67',
        query='#NFT -is:reply -is:retweet -"drop your" -giveaway lang:en -"show me your"',
        max_results=max_results,
        user_fields=['public_metrics'],
        expansions=['author_id'],
        tweet_fields=['created_at'],

    )


if __name__ == "__main__":
    main()
    print("liked tweets")
