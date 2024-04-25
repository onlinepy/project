import csv

class BankAccount:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            return True
        return False

    def transfer(self, other_account, amount):
        if self.balance >= amount:
            self.balance -= amount
            other_account.balance += amount
            return True
        return False

    def save_to_csv(self, file_path):
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.name, self.balance])

    @staticmethod
    def load_from_csv(file_path):
        accounts = []
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                name, balance = row
                account = BankAccount(name, int(balance))
                accounts.append(account)
        return accounts

# 创建账户
account1 = BankAccount("Alice", 1000)
account2 = BankAccount("Bob", 500)

# 存款
account1.deposit(500)

# 取款
account1.withdraw(200)

# 转账
account1.transfer(account2, 300)

# 保存账户状态到CSV
account1.save_to_csv('bank_accounts.csv')
account2.save_to_csv('bank_accounts.csv')

# 加载账户状态
loaded_accounts = BankAccount.load_from_csv('bank_accounts.csv')
for account in loaded_accounts:
    print(f"Name: {account.name}, Balance: {account.balance}")