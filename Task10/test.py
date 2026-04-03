from wallet import Wallet
from transaction import Transaction
from blockchain import Blockchain
bc = Blockchain()

vicky = Wallet()
maha = Wallet()

print("---Wallets---")
print("Wallet 1 Address:",vicky.get_address)
print(f"Before Transaction({vicky.get_address}):",bc.get_balance(vicky.get_address()))
print("Wallet 2 Address:",maha.get_address)
print(f"Before Transaction({maha.get_address()}):",bc.get_balance(maha.get_address()))

tx = Transaction(
    vicky.get_address(),
    maha.get_address(),
    10
)

tx.sign_transaction(vicky)

print("Transaction signature:")
print(tx.signature)

bc.add_transaction(tx)
bc.mine_pending_transactions()
print(f"After Transaction({maha.get_address()}):",bc.get_balance(maha.get_address()))
print(f"After Transaction({maha.get_address()}):",bc.get_balance(vicky.get_address()))

