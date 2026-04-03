import hashlib

def mine_block(block, difficulty):
    prefix = "0" * difficulty
    while True:
        hash_value = block.calculate_hash()
        if hash_value.startswith(prefix):
            return hash_value
        block.nonce += 1