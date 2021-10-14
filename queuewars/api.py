import requests
import time
import json
import config
import sys

from numpy import random

BETA = 0.04

AVAILABLE_TEAMS = ['one', 'two', 'three', 'four', 'five', 'six']

if not config.OWNER in AVAILABLE_TEAMS:
    print(f"Incorrect owner '{config.OWNER}' in config.py file.")
    print(f"Available ones: {', '.join(AVAILABLE_TEAMS)}.")
    sys.exit(-1)

def fetch_next(scrollId):
    url = "{}/api/chunk/{}".format(config.BASE_URL, scrollId)
    print('GET', url)
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        else:
            print("Error fetching", scrollId)
    except requests.exceptions.ConnectionError as ex:
        print(ex)
    return None

def fetch():
    scrollId = 0
    while True:
        data = fetch_next(scrollId)
        if data is None:
            return
        chunks = data['data']
        for chunk in chunks:
            chunk['page'] = scrollId
            yield chunk
        if BETA:
            time.sleep(random.exponential(BETA))
        scrollId += 1

def confirm(block_id, chunk_ids):
    print("Confirming block", block_id, "with chunks:", chunk_ids)
    if BETA:
        time.sleep(random.exponential(BETA))
    url = "{}/api/block/{}".format(config.BASE_URL, block_id)
    owner = config.OWNER
    try:
        r = requests.post(url, json = { 'block_id': block_id, 'chunks': chunk_ids, 'owner': owner })
        status_code = r.status_code
        text = r.text
    except requests.exceptions.ConnectionError as ex:
        status_code = -200
        text = ex.message if hasattr(ex, 'message') else ex
    if status_code == 200:
        print("Confirmed:", block_id)
    else:
        print("Rejected:", block_id, status_code, text)
    return status_code

def fetch_confirmed():
    url = "{}/api/blocks".format(config.BASE_URL)
    try:
        r = requests.get(url)
        confirmed_blocks = json.loads(r.text)
        confirmed_blocks = { int(k): v for k, v in confirmed_blocks.items() }
    except requests.exceptions.ConnectionError as ex:
        confirmed_blocks = {}
        print(ex)
    return confirmed_blocks

def main():
    chunks = fetch()
    for chunk in chunks:
        print(chunk)
    confirm(1593, ["4b41ae", "671aca", "fb4621"])

if __name__ == '__main__':
    main()
