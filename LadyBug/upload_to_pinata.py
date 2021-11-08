"""
Pin any file, or directory, to Pinata's IPFS nodes
More: https://docs.pinata.cloud/api-pinning/pin-file
"""
import os
import json
import requests

API_ENDPOINT = "https://api.pinata.cloud/"

Header = {
    'pinata_api_key': "<PINATA_API_KEY>",
    'pinata_secret_api_key': "<PINATA_SECRET_API_KEY>"
}

url = API_ENDPOINT + "pinning/pinFileToIPFS"
img_path = os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), './output')

hash_response = []

for img in os.listdir(img_path):
    path_to_file = img_path + '/' + img
    file = {'file': open(path_to_file, "rb")}
    response: requests.Response = requests.post(url=url, files=file, headers=Header)
    if response.ok:
        hash_response.append(response.json())

with open('hashresponse.txt', 'w') as f:
    f.write(json.dumps(hash_response))

