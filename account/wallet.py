class Wallet:
    def __init__(self, balance: int = 5000):
        self.balance = balance

    def add(self, amount: int):
        self.balance += amount

    def subtract(self, amount: int) -> bool:
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

    def get_balance(self) -> int:
        return self.balance
