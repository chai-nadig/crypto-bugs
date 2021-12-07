import json
from tweet import construct_tweet

with open('facts.json', 'r') as f:
    facts = json.load(f)

for i in range(len(facts)):
    tweet, hash_tag_count = construct_tweet(i + 1, facts[i])

    if len(tweet) > 280:
        print(len(tweet) - 280, tweet)

    print(tweet)
    assert hash_tag_count != 0
