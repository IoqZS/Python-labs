class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False

    def get_balance(self):
        return self._balance

    def calculate_income(self):
        return 0

    def get_info(self):
        return f"{self.owner}: баланс {self._balance:.2f}"


class DebitAccount(BankAccount):
    def calculate_income(self):
        return 0


class SavingsAccount(BankAccount):
    def __init__(self, owner, balance, rate):
        super().__init__(owner, balance)
        self.rate = rate

    def calculate_income(self):
        return self._balance * self.rate / 100


class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = []

    def add(self, account):
        self.accounts.append(account)

    def show(self):
        for account in self.accounts:
            print(
                f"{account.get_info()}, "
                f"доход: {account.calculate_income():.2f}"
            )


def main():
    first = DebitAccount("Иван", 10000)
    second = SavingsAccount("Анна", 20000, 5)
    third = SavingsAccount("Сергей", 30000, 7)

    first.deposit(2000)
    second.withdraw(5000)

    bank = Bank("Учебный банк")
    bank.add(first)
    bank.add(second)
    bank.add(third)

    bank.show()


if __name__ == "__main__":
    main()
