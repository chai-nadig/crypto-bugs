import json
import os
from os.path import isfile, join
import random

import tweepy
from json.decoder import JSONDecodeError
from PIL import Image
from telegram_bot import send_message, batch_telegram_messages

READ_FILE = './facts.json'
TWEETED_FILE = './tweeted-facts.json'
DISCARDED_FILE = './discarded-facts.json'


# READ_FILE = './tweets.json'
# TWEETED_FILE = './tweeted-tweets.json'
# DISCARDED_FILE = './discarded-tweets.json'


@batch_telegram_messages()
def main():
    send_message("<b>Tweeting</b>")

    tweet_number = get_count_tweeted() + 1
    send_message("Sending tweet_number: {}".format(tweet_number))

    random_tweet, idx = get_random_tweet()

    if random_tweet is None:
        send_message("no tweets to tweet")
        return

    send_message("Tweet: {}".format(random_tweet))

    img_file_name, img_relative_path = get_next_image()
    if img_relative_path is None:
        send_message("no image to tweet")
        return

    resize_and_save(img_relative_path)

    media = upload_media(img_file_name, img_relative_path)

    tweeted = False
    while not tweeted and random_tweet:
        tweet_content, _ = construct_tweet(random_tweet, tweet_number=tweet_number)
        tweeted = tweet(tweet_content, media_ids=[media.media_id])

        if not tweeted:
            send_message("Discarding: {}".format(random_tweet))
            discard_tweet(random_tweet)
            remove_tweet(idx)

            random_tweet, idx = get_random_tweet()
            if random_tweet is None:
                send_message("no tweets to tweet")
                return

            send_message("Another Tweet: {}".format(random_tweet))

    save_tweeted_tweet(random_tweet)
    remove_tweet(idx)
    remove_image(img_file_name)

    user = get_crypto_bugs_user()
    send_message("<b>Followers: {}</b>".format(user.public_metrics['followers_count']))


def remove_image(img_file_name):
    os.rename('./images/{}'.format(img_file_name), './uploaded_images/{}'.format(img_file_name))


def get_next_image():
    onlyfiles = [f for f in os.listdir('./images') if isfile(join('./images', f))]
    if len(onlyfiles) == 0:
        return None, None

    filename = random.choices(onlyfiles)[0]
    return filename, './images/{}'.format(filename)


def resize_and_save(img_relative_path):
    img = Image.open(img_relative_path).convert('RGBA')
    img = img.resize((240, 240), Image.NEAREST)
    img.save(img_relative_path)


def remove_tweet(idx):
    if idx is None:
        return

    with open(READ_FILE) as f:
        tweets = json.load(f)

    tweets.pop(idx)

    with open(READ_FILE, 'w') as f:
        json.dump(tweets, f, indent=4)


def get_random_tweet():
    with open(READ_FILE) as f:
        tweets = json.load(f)

    if len(tweets) == 0:
        return None, None

    idx = random.randint(0, len(tweets) - 1)
    random_tweet = tweets[idx]

    return random_tweet, idx


def get_tweeted_tweets():
    tweeted_tweets = []
    with open(TWEETED_FILE) as f:
        try:
            tweeted_tweets = json.load(f)
        except JSONDecodeError:
            pass

    return tweeted_tweets


def get_count_tweeted():
    tweeted_tweets = get_tweeted_tweets()
    return len(tweeted_tweets)


def save_tweeted_tweet(tweeted_tweet):
    if tweeted_tweet is None:
        return

    tweeted_tweets = get_tweeted_tweets()
    tweeted_tweets.append(tweeted_tweet)

    with open(TWEETED_FILE, 'w') as f:
        json.dump(tweeted_tweets, f, indent=4)


def get_discarded_tweet():
    discarded_tweets = []
    with open(DISCARDED_FILE) as f:
        try:
            discarded_tweets = json.load(f)
        except JSONDecodeError:
            pass

    return discarded_tweets


def discard_tweet(tw):
    discarded_tweets = get_discarded_tweet()
    discarded_tweets.append(tw)

    with open(DISCARDED_FILE, 'w') as f:
        json.dump(discarded_tweets, f, indent=4)


def construct_tweet(tw, tweet_number=None):
    hash_tags = [
        "#NFT", "#CryptoBugs", "#Ladybug", "#NFTCommunity",
        "#NFTs", "#NFTCollector", "#NFTCollectibles",
        "#NFTCollectible", "#DigitalArt", "#LadyBird",
        "#FunFact",
    ]

    content = (
        "🐞 Ladybug Fun Fact #{}: {} 🐞"
    ).format(tweet_number, tw)

    # content = (
    #     "🐞 {} 🐞"
    # ).format(tw)

    hash_tag_count = 0
    for i in range(len(hash_tags)):
        if i == 0:
            tag = "\n\n{}".format(hash_tags[i])
        else:
            tag = " {}".format(hash_tags[i])

        if len(content) + len(tag) <= 280:
            hash_tag_count += 1
            content = content + tag

    return content, hash_tag_count


def upload_media(img_file_name, img_relative_path):
    twitter_auth_keys = {
        "consumer_key": os.getenv('TWITTER_CONSUMER_KEY'),
        "consumer_secret": os.getenv('TWITTER_CONSUMER_SECRET'),
        "access_token": os.getenv('TWITTER_ACCESS_TOKEN'),
        "access_token_secret": os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
    }

    auth = tweepy.OAuthHandler(
        twitter_auth_keys['consumer_key'],
        twitter_auth_keys['consumer_secret']
    )
    auth.set_access_token(
        twitter_auth_keys['access_token'],
        twitter_auth_keys['access_token_secret']
    )
    api = tweepy.API(auth)

    with open(img_relative_path, 'rb') as img:
        media = api.media_upload(img_file_name, file=img, media_category="TWEET_IMAGE")

    return media


def tweet(content, media_ids=None, in_reply_to_tweet_id=None):
    if len(content) > 280:
        return False

    client = tweepy.Client(
        consumer_key=os.getenv('TWITTER_CONSUMER_KEY'),
        consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET'),
        access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
        access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
    )

    response = client.create_tweet(
        text=content,
        media_ids=media_ids,
        in_reply_to_tweet_id=in_reply_to_tweet_id,
    )

    return response.data['id']


def get_crypto_bugs_user():
    client = tweepy.Client(bearer_token=os.getenv('TWITTER_BEARER_TOKEN'))

    user = client.get_user(
        username='CryptoBugsX2B67',
        user_fields="public_metrics",
    )

    return user.data


if __name__ == "__main__":
    main()
    print("Ladybug Fun Fact")
