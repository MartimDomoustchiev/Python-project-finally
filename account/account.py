from .wallet import Wallet

class Account:
    def __init__(self, username: str, balance: int = 5000):
        self.username = username
        self.wallet = Wallet(balance)

    def get_username(self):
        return self.username

    def get_balance(self):
        return self.wallet.get_balance()

    def deposit(self, amount: int):
        self.wallet.add(amount)

    def withdraw(self, amount: int) -> bool:
        return self.wallet.subtract(amount)
