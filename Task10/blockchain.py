from block import Block
from proofofwork   import mine_block

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 4
        self.pending_transactions = []
        self.create_genesis_block()


    def create_genesis_block(self):
        genesis = Block([], "0")
        genesis.hash = genesis.calculate_hash()
        self.chain.append(genesis)

    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self):
        block = Block(
            self.pending_transactions,
            self.get_last_block().hash
        )
        block.hash = mine_block(block, self.difficulty)
        self.chain.append(block)
        self.pending_transactions = []
        
    def get_balance(self, address):
        balance = 20
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == address:
                    balance -= tx.amount
                if tx.receiver == address:
                    balance += tx.amount
        return balance