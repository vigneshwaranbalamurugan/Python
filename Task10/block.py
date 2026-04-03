import time
import hashlib
from merkletree import merkle_root

class Block:
    def __init__(self, transactions, previous_hash):
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.merkle_root = merkle_root(transactions)
        self.hash = None

    def calculate_hash(self):
        data = (
            str(self.timestamp)
            + str(self.previous_hash)
            + str(self.nonce)
            + str(self.merkle_root)
        )

        return hashlib.sha256(data.encode()).hexdigest()