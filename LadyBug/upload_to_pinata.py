"""
Pin any file, or directory, to Pinata's IPFS nodes
More: https://docs.pinata.cloud/api-pinning/pin-file
"""
import requests
from tqdm import tqdm
import json

Header = {
    'pinata_api_key': "480276fcf43ffc03f46b",
    'pinata_secret_api_key': "e9a4967cbc3145ab184e9dab29c1028ca64d9ae1a5a1d09e7581d2d32bb99d38"
}

url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

directory = "./output"


def upload_to_pinata(traits_file):
    traits = json.loads(traits_file)

    total = len(traits)

    with tqdm(total=total, desc='Uploading {} images to pinata'.format(total), unit="images") as pbar:
        for trait in traits:
            fileName = '{}/{}.png'.format(directory, trait['tokenId'])

            file = {'file': open(fileName, "rb")}

            response = requests.post(url=url, files=file, headers=Header)

            body = response.json()

            if response.ok:
                trait['imageIPFS'] = body['IpfsHash']

            else:
                print("something went wrong")

            pbar.update(1)

    return traits


traits = json.loads('traits.json')


print(traits)