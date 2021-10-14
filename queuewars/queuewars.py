import api
import config

def main():
    blocks = {}
    confirmed = api.fetch_confirmed()
    chunks = api.fetch()

    for chunk in chunks:
        block_id = chunk["parent"]
        if block_id not in confirmed:
            if block_id not in blocks:
                blocks[block_id] = { "weight": 0, "chunks": [] }
            b = blocks[block_id]
            b["weight"] += chunk["weight"]
            b["chunks"].append(chunk["id"])
            if b["weight"] >= 1. and api.confirm(block_id, b["chunks"]) == 200:
                confirmed[block_id] = config.OWNER
    
    num_received = len(blocks)
    num_confirmed = len(api.fetch_confirmed())
    print("%d blocks confirmed and %d received" % (num_confirmed, num_received))
    if num_received > 0:
        print("%f%%" % (num_confirmed / num_received * 100))
    print("Missing blocks:", sorted(filter(lambda bk: bk not in confirmed.keys(), blocks.keys())))

if __name__ == '__main__':
    main()
