import json
import os
import random
from json import JSONDecodeError

import tweepy
from telegram_bot import send_message, batch_telegram_messages


@batch_telegram_messages()
def main():
    send_message("<b>Unfollowing users</b>")

    followed_authors = get_followed_authors()
    subset_followed = random.choices(followed_authors, k=50)

    unfollowed = []
    verified_users = []

    try:

        for followed_user_id in subset_followed:
            user = get_twitter_user(followed_user_id)

            if not user:
                unfollowed.append(followed_user_id)
            elif not user.verified:
                unfollow(user.id)
                unfollowed.append(user.id)
            else:
                verified_users.append(user.id)

    except Exception as e:
        send_message("error unfollowing users: {}".format(str(e)))

    currently_followed = [user for user in followed_authors if user not in unfollowed]

    save_followed_authors(currently_followed)

    save_verified_users(verified_users)

    send_message("unfollowed {} users".format(len(unfollowed)))

    user = get_crypto_bugs_user()

    send_message("<b>Followers: {}</b>".format(user.public_metrics['followers_count']))
    send_message("<b>Following: {}</b>".format(user.public_metrics['following_count']))


def get_crypto_bugs_user():
    client = tweepy.Client(bearer_token=os.getenv('TWITTER_BEARER_TOKEN'))

    user = client.get_user(
        username='CryptoBugsX2B67',
        user_fields="public_metrics",
    )

    return user.data


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

    with open('./followed-authors.json', 'w') as f:
        json.dump(followed_authors, f, indent=4)


def get_verified_users():
    verified_authors = []
    with open('./verified-authors.json') as f:
        try:
            verified_authors = json.load(f)
        except JSONDecodeError:
            pass

    return verified_authors


def save_verified_users(verified_users):
    if len(verified_users) == 0:
        return

    already_verified_users = get_verified_users()
    already_verified_users.extend(verified_users)

    with open('./verified-users.json', 'w') as f:
        json.dump(already_verified_users, f, indent=4)


def get_twitter_user(user_id):
    client = tweepy.Client(bearer_token=os.getenv('TWITTER_BEARER_TOKEN'))

    user = client.get_user(
        id=user_id,
        user_fields=["public_metrics", "verified"],
    )

    return user.data


def unfollow(user_id):
    client = tweepy.Client(
        consumer_key=os.getenv('TWITTER_CONSUMER_KEY'),
        consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET'),
        access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
        access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
    )

    client.unfollow_user(user_id)


if __name__ == "__main__":
    main()
    print("unfollowed users")
