import json
import random

import tweepy
from json.decoder import JSONDecodeError
from PIL import Image


def main():
    fact, idx = get_next_fact()
    fact_number = get_next_fact_number()

    print(fact)
    print(fact_number)

    img_file_name = '{}.png'.format(fact_number - 1)
    img_relative_path = './images/{}'.format(img_file_name)

    resize_and_save(img_relative_path)

    tweeted = False
    while not tweeted:
        tweeted = tweet(fact_number, fact, img_file_name, img_relative_path)
        if not tweeted:
            discard_fact(fact)

    save_tweeted_fact(fact)

    remove_fact(idx)


def resize_and_save(img_file_name):
    img = Image.open(img_file_name).convert('RGBA')
    img = img.resize((240, 240), Image.NEAREST)
    img.save(img_file_name)


def remove_fact(idx):
    with open('./facts.json') as f:
        facts = json.load(f)

    facts.pop(idx)

    with open('./facts.json', 'w') as f:
        json.dump(facts, f, indent=4)


def get_next_fact():
    with open('./facts.json') as f:
        facts = json.load(f)

    if len(facts) == 0:
        return None

    idx = random.randint(0, len(facts) - 1)
    fact = facts[idx]

    return fact, idx


def get_tweeted_facts():
    tweeted_facts = []
    with open('./tweeted-facts.json') as f:
        try:
            tweeted_facts = json.load(f)
        except JSONDecodeError:
            pass

    return tweeted_facts


def get_next_fact_number():
    tweeted_facts = get_tweeted_facts()
    return len(tweeted_facts) + 1


def save_tweeted_fact(fact):
    tweeted_facts = get_tweeted_facts()
    tweeted_facts.append(fact)

    with open('./tweeted-facts.json', 'w') as f:
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


def tweet(fact_number, fact, img_file_name, img_relative_path):
    twitter_auth_keys = {
        "consumer_key": "s2SyD5Gs7Yi6gU3z5UujPbcuf",
        "consumer_secret": "mzWhAHI5rquSJBJiRPfN8H3gw2besSny0tqqDz4F3rhTFVvPQO",
        "access_token": "1457120903695724545-Hhs0zB7Rv8flgetNXgPZa2fDeKQnwv",
        "access_token_secret": "p2oPz4FuwvgfdpchldFX3LhWEWWFdXGaawp31fF1Adhoo"
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

    content = (
        "🐞 Ladybug Fun Fact #{}: {}🐞\n\n"
        "#NFT #NFTs #NFTCollector #NFTCollectibles "
        "#NFTCollectible #NFTCommunity #DigitalArt #CryptoBugs #FunFact #LadyBird #Ladybug"
    ).format(fact_number, fact)

    if len(content) > 280:
        return False

    with open(img_relative_path, 'rb') as img:
        media = api.media_upload(img_file_name, file=img, media_category="TWEET_IMAGE")

    status = api.update_status(status=content, media_ids=[media.media_id])

    print(status.entities['urls'][0]['expanded_url'])

    return True


if __name__ == "__main__":
    main()
    print("Ladybug Fun Fact")
