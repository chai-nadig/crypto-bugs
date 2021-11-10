"""
Pin any file, or directory, to Pinata's IPFS nodes
More: https://docs.pinata.cloud/api-pinning/pin-file
"""
from multiprocessing import Pool
from time import sleep

import requests
from tqdm import tqdm
import json

Header = {
    'pinata_api_key': "480276fcf43ffc03f46b",
    'pinata_secret_api_key': "e9a4967cbc3145ab184e9dab29c1028ca64d9ae1a5a1d09e7581d2d32bb99d38"
}

url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

directory = "./output"


def _upload(trait):
    fileName = '{}/{}.png'.format(directory, trait['tokenId'])
    file = {'file': open(fileName, "rb")}

    try:

        response = requests.post(url=url, files=file, headers=Header)
        body = response.json()

        if response.ok:
            trait['imageIPFS'] = body['IpfsHash']
        else:
            print("something went wrong", fileName, json.dumps(response))

    except Exception as e:
        print(e)

    sleep(3)
    return trait


def upload_to_pinata(traits_file):
    with open(traits_file) as f:
        traits = json.load(f)

    total = len(traits)

    with Pool(10) as p:
        traits_with_ipfs_hash = list(tqdm(p.imap(_upload, traits), total=total))

    traits = sorted(traits_with_ipfs_hash, key=lambda t: t['tokenId'])

    assert len(traits) == total
    for trait in traits:
        assert len(trait['imageIPFS']) > 0

    return traits
