import json
import os
import random
from collections import defaultdict
from json import JSONDecodeError

import backoff as backoff
import tweepy
from tweet import (
    get_next_image,
    resize_and_save,
    upload_media,
    tweet,
    remove_image,
)

"""
1. Get Tweets after previous max id
2. Filter tweets by users with large number of followers
    2.1 Map tweets by author
    2.2 Select tweets by authors with large followers

3. Reply to tweet with image and hash tags
4. Move image to different folder
5. Save Max tweet id


"""

# Limit specified by twitter
# 50 requests per 15 min window
# user limit: 400 successful requests per 24-hour window
# app limit: 1000 successful requests per 24-hou
FOLLOW_LIMIT = 50

# We only want to reply to tweets by authors having more than this number of followers
FOLLOWERS_THRESHOLD = 1000


def main():
    max_tweet_id = get_max_tweet_id()

    response = get_tweets('-is:retweet -is:reply "drop your" (nft OR nfts)', since_id=max_tweet_id)

    if response.data is None or len(response.data) == 0:
        print("no new recent tweets found")
        return

    max_tweet_id = max([tw.id for tw in response.data])

    save_max_tweet_id(max_tweet_id)

    tweets_by_author = get_tweets_by_author(response.data)

    tweets_by_popular_authors = get_tweets_by_popular_authors(tweets_by_author, response.includes['users'])

    tweets_by_unpopular_authors = get_tweets_by_unpopular_authors(tweets_by_author, response.includes['users'])

    print("number tweets popular authors", sum([len(tweets) for author, tweets in tweets_by_popular_authors.items()]))

    print("number tweets unpopular authors",
          sum([len(tweets) for author, tweets in tweets_by_unpopular_authors.items()]))

    if len(tweets_by_popular_authors) == 0 and len(tweets_by_unpopular_authors) == 0:
        print("no tweets from popular authors or unpopular authors found")
        return

    followed_authors = follow_authors(list(tweets_by_popular_authors.keys()))

    if len(followed_authors) > 0:
        print("followed {} new authors".format(len(followed_authors)))

    save_followed_authors(followed_authors)

    for author_id, tweets in tweets_by_popular_authors.items():
        for tw in tweets:
            try:
                img_file_name, img_relative_path = get_next_image()
                if img_relative_path is None:
                    print("no image to tweet")
                    return

                resize_and_save(img_relative_path)

                media = upload_media(img_file_name, img_relative_path)

                random_tweet = get_random_tweet()

                tweet_reply_content = construct_tweet_reply(random_tweet)

                r = tweet(tweet_reply_content, media_ids=[media.media_id], in_reply_to_tweet_id=tw.id)

                print(r)

                remove_image(img_file_name)

            except Exception as e:
                print("error processing tweet by popular author", e, author_id, tw)

    for author_id, tweets in tweets_by_unpopular_authors.items():
        should_break = False
        for tw in tweets:
            try:
                replies = get_tweets('conversation_id:{} is:reply -"promote it on" '.format(tw.id))

                if replies.data is None or len(replies.data) == 0:
                    continue

                for reply in replies.data:
                    like_tweet(reply)
                    print("liked {}".format(reply.id))

            except tweepy.TooManyRequests:
                print("too many likes posted")
                should_break = True
                break

            except Exception as e:
                print("error processing tweet by unpopular author", e, author_id, tw)

        if should_break:
            break


def like_tweet(tw):
    client = tweepy.Client(
        consumer_key=os.getenv('TWITTER_CONSUMER_KEY'),
        consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET'),
        access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
        access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
    )

    return client.like(tw.id)


def get_authors_with_liked_tweets():
    authors_with_liked_tweets = []
    with open('./authors-with-liked-tweets.json') as f:
        try:
            authors_with_liked_tweets = json.load(f)
        except JSONDecodeError:
            pass

    return authors_with_liked_tweets


def save_authors_with_liked_tweets(authors_with_liked_tweets):
    if len(authors_with_liked_tweets) == 0:
        return

    already_liked_authors = get_authors_with_liked_tweets()
    already_liked_authors.extend(authors_with_liked_tweets)

    with open('./authors-with-liked-tweets.json', 'w') as f:
        json.dump(already_liked_authors, f, indent=4)


def get_max_tweet_id():
    max_tweet_id = None
    with open('./max-tweet-id.json') as f:
        try:
            max_tweet_id = json.load(f)
        except JSONDecodeError:
            pass

    return max_tweet_id


def save_max_tweet_id(max_tweet_id):
    with open('./max-tweet-id.json', 'w') as f:
        json.dump(max_tweet_id, f, indent=4)


def construct_tweet_reply(tw):
    hash_tags = [
        "#NFT", "#CryptoBugs", "#Ladybug", "#NFTCommunity",
        "#NFTs", "#NFTCollector", "#NFTCollectibles",
        "#NFTCollectible", "#DigitalArt", "#LadyBird",
    ]

    content = (
        "🐞 {} 🐞"
    ).format(tw)

    hash_tag_count = 0
    for i in range(len(hash_tags)):
        if i == 0:
            tag = "\n\n{}".format(hash_tags[i])
        else:
            tag = " {}".format(hash_tags[i])

        if len(content) + len(tag) <= 280:
            hash_tag_count += 1
            content = content + tag

    return content


def get_tweets_by_author(tweets):
    tweets_by_author = defaultdict(list)
    for tweet in tweets:
        tweets_by_author[tweet.author_id].append(tweet)

    return tweets_by_author


def is_author_popular(author):
    return author.public_metrics['followers_count'] > FOLLOWERS_THRESHOLD or author.verified


def get_tweets_by_popular_authors(tweets_by_author, authors):
    tweets_by_popular_authors = defaultdict(list)
    for author in authors:
        if is_author_popular(author):
            tweets_by_popular_authors[author.id] = tweets_by_author[author.id]

    return tweets_by_popular_authors


def get_tweets_by_unpopular_authors(tweets_by_author, authors):
    tweets_by_unpopular_authors = defaultdict(list)
    for author in authors:
        if not is_author_popular(author):
            tweets_by_unpopular_authors[author.id] = tweets_by_author[author.id]

    return tweets_by_unpopular_authors


def follow_authors(author_ids):
    already_followed_authors = set(get_followed_authors())

    limited_author_ids = [author_id for author_id in author_ids if author_id not in already_followed_authors]
    limited_author_ids = limited_author_ids[:FOLLOW_LIMIT]

    if len(limited_author_ids) == 0:
        print("no new popular authors to follow")
        return []

    followed_authors = []

    for author_id in limited_author_ids:
        try:
            follow_author(author_id)
            followed_authors.append(author_id)
        except Exception as e:
            print(e, author_id)

    return followed_authors


def get_followed_authors():
    followed_authors = []
    with open('./followed-authors.json') as f:
        try:
            followed_authors = json.load(f)
        except JSONDecodeError:
            pass

    return followed_authors


def save_followed_authors(followed_authors):
    if len(followed_authors) == 0:
        return

    already_followed_authors = get_followed_authors()
    already_followed_authors.extend(followed_authors)

    with open('./followed-authors.json', 'w') as f:
        json.dump(already_followed_authors, f, indent=4)


@backoff.on_exception(backoff.expo, tweepy.TooManyRequests, max_time=5)
def follow_author(author_id):
    client = tweepy.Client(
        consumer_key=os.getenv('TWITTER_CONSUMER_KEY'),
        consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET'),
        access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
        access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
    )

    return client.follow_user(author_id)


def get_tweets(query, max_results=100, since_id=None):
    client = tweepy.Client(bearer_token=os.getenv('TWITTER_BEARER_TOKEN'))

    tweets = client.search_recent_tweets(
        query=query,
        max_results=max_results,
        user_fields=['public_metrics', 'verified'],
        expansions=['author_id'],
        tweet_fields=['created_at'],
        since_id=since_id,
    )

    return tweets


def get_random_tweet():
    with open('./tweets.json') as f:
        facts = json.load(f)

    with open('./tweeted-tweets.json') as f:
        facts.extend(json.load(f))

    return random.choice(facts)


if __name__ == "__main__":
    main()
    print("Dropped our NFT")
