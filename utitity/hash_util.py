import hashlib
import json


def hash_block(block):
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [tx.to_ordered_dict() for tx in hashable_block['transactions']]
    hashed_block = json.dumps(hashable_block).encode()
    return hashlib.sha256(hashed_block).hexdigest()