import json
import hashlib

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = None

    def calculate_hash(self):
        data = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()

    def sign_transaction(self, wallet):
        self.signature = wallet.sign_transaction(self.calculate_hash())