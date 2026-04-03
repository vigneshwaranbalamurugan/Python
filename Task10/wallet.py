import ecdsa
import hashlib

class Wallet:
    def __init__(self):
        self.private_key = ecdsa.SigningKey.generate()
        self.public_key = self.private_key.get_verifying_key()

    def sign_transaction(self, message):
        return self.private_key.sign(message.encode()).hex()

    def get_address(self):
        return hashlib.sha256(self.public_key.to_string()).hexdigest()