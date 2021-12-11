import json
import os
from os.path import isfile, join
import random

import tweepy
from json.decoder import JSONDecodeError
from PIL import Image


def main():
    fact_number = get_next_fact_number()
    print(fact_number)

    fact, idx = get_next_fact()
    print(fact)

    if fact is None:
        print("no facts to tweet")
        return

    img_file_name, img_relative_path = get_next_image()
    if img_relative_path is None:
        print("no image to tweet")
        return

    resize_and_save(img_relative_path)

    media = upload_media(img_file_name, img_relative_path)

    tweeted = False
    while not tweeted and fact:
        tweet_content, _ = construct_tweet(fact_number, fact)
        tweeted = tweet(tweet_content, media_ids=[media.media_id])

        if not tweeted:
            discard_fact(fact)
            remove_fact(idx)

            fact, idx = get_next_fact()
            print(fact)

            if fact is None:
                print("no facts to tweet")
                return

    save_tweeted_fact(fact)
    remove_fact(idx)
    remove_image(img_file_name)


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


def remove_fact(idx):
    if idx is None:
        return

    with open('./tweets.json') as f:
        facts = json.load(f)

    facts.pop(idx)

    with open('./tweets.json', 'w') as f:
        json.dump(facts, f, indent=4)


def get_next_fact():
    with open('./tweets.json') as f:
        facts = json.load(f)

    if len(facts) == 0:
        return None, None

    idx = random.randint(0, len(facts) - 1)
    fact = facts[idx]

    return fact, idx


def get_tweeted_facts():
    tweeted_facts = []
    with open('./tweeted-tweets.json') as f:
        try:
            tweeted_facts = json.load(f)
        except JSONDecodeError:
            pass

    return tweeted_facts


def get_next_fact_number():
    tweeted_facts = get_tweeted_facts()
    return len(tweeted_facts) + 1


def save_tweeted_fact(fact):
    if fact is None:
        return

    tweeted_facts = get_tweeted_facts()
    tweeted_facts.append(fact)

    with open('./tweeted-tweets.json', 'w') as f:
        json.dump(tweeted_facts, f, indent=4)


def get_discarded_facts():
    discarded_facts = []
    with open('./discarded-facts.json') as f:
        try:
            discarded_facts = json.load(f)
        except JSONDecodeError:
            pass

    return discarded_facts


def discard_fact(fact):
    discarded_facts = get_discarded_facts()
    discarded_facts.append(fact)

    with open('./discarded-facts.json', 'w') as f:
        json.dump(discarded_facts, f, indent=4)


def construct_tweet(fact_number, fact):
    hash_tags = ["#NFT", "#CryptoBugs", "#Ladybug", "#FunFact", "#NFTCommunity",
                 "#NFTs", "#NFTCollector", "#NFTCollectibles",
                 "#NFTCollectible", "#DigitalArt", "#LadyBird"]
    # content = (
    #     "🐞 Ladybug Fun Fact #{}: {} 🐞"
    # ).format(fact_number, fact)

    content = (
        "🐞 {} 🐞"
    ).format(fact)

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


if __name__ == "__main__":
    main()
    print("Ladybug Fun Fact")
