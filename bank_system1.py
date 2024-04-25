# !/usr/bin/python
# -*- coding: utf-8 -*-

"""
@File: bank_system.py
@Author: Zaiqiang
@Date: April 25, 2024
@Description: A simple bank system implementation in Python
@Version: 1.0.1
"""
import csv
import logging
from datetime import datetime
from uuid import uuid4

# 用户身份验证类
class AuthenticationService:
    def __init__(self):
        self.users = {}  # 用户字典，键是用户名，值是密码

    def register(self, username, password):
        if not username or not password:
            raise ValueError("Username and password must not be empty.")
        if username in self.users:
            raise ValueError("Username already exists.")
        self.users[username] = password

    def login(self, username, password):
        if username not in self.users or self.users[username] != password:
            raise ValueError("Invalid username or password.")
        return True

# 日志记录类
class TransactionLogger:
    def __init__(self, file_path):
        self.file_path = file_path

    def log(self, user, account, action, amount, success):
        with open(self.file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now(), user.username, account.account_number, action, amount, success])

# 账户类
class Account:
    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        if amount > self.balance:
            raise ValueError("Insufficient balance.")
        self.balance -= amount

# 用户类
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)

# 银行系统类
class Bank:
    def __init__(self):
        self.users = []

    def create_user(self, username, password):
        if not username or not password:
            raise ValueError("Username and password must not be empty.")
        user = User(username, password)
        self.users.append(user)
        return user

    def create_account(self, user, account_number, balance):
        if not account_number or len(account_number) != 5:
            raise ValueError("Account number must be a 5-digit string.")
        account = Account(account_number, balance)
        user.add_account(account)
        return account

    def deposit(self, user, account, amount):
        if user not in self.users:
            raise ValueError("User not found.")
        account.deposit(amount)

    def withdraw(self, user, account, amount):
        if user not in self.users:
            raise ValueError("User not found.")
        account.withdraw(amount)

    def transfer(self, user_from, account_from, user_to, account_to, amount):
        if user_from not in self.users or user_to not in self.users:
            raise ValueError("User not found.")
        if account_from not in user_from.accounts or account_to not in user_to.accounts:
            raise ValueError("Account not found.")
        self.withdraw(user_from, account_from, amount)
        self.deposit(user_to, account_to, amount)

    def save_state_to_csv(self, file_path):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'password', 'account_number', 'balance'])
            for user in self.users:
                for account in user.accounts:
                    writer.writerow([user.username, user.password, account.account_number, account.balance])

    def load_state_from_csv(self, file_path):
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # 跳过标题行
            for row in reader:
                username, password, account_number, balance = row
                user = self.create_user(username, password)
                account = self.create_account(user, account_number, int(balance))

# 主程序
if __name__ == "__main__":
    auth_service = AuthenticationService()
    logger = TransactionLogger('transactions.csv')
    bank = Bank()

    # 用户注册和登录
    try:
        auth_service.register('user1', 'pass1')
        user = auth_service.login('user1', 'pass1')
    except ValueError as e:
        print(e)
        exit(1)

    # 创建用户
    try:
        user = bank.create_user('Alice', 'pass1')
    except ValueError as e:
        print(e)
        exit(1)

    # 创建账户
    try:
        account = bank.create_account(user, '12345', 1000)
    except ValueError as e:
        print(e)
        exit(1)

    # 存款
    try:
        bank.deposit(user, account, 500)
        logger.log(user, account, 'deposit', 500, True)
    except ValueError as e:
        print(e)
        logger.log(user, account, 'deposit', 500, False)
        exit(1)

    # 取款
    try:
        bank.withdraw(user, account, 200)
        logger.log(user, account, 'withdraw', 200, True)
    except ValueError as e:
        print(e)
        logger.log(user, account, 'withdraw', 200, False)
        exit(1)

    # 转账
    try:
        other_user = bank.create_user('Bob', 'pass2')
        other_account = bank.create_account(other_user, '67890', 0)
        bank.transfer(user, account, other_user, other_account, 300)
        logger.log(user, account, 'transfer', 300, True)
    except ValueError as e:
        print(e)
        logger.log(user, account, 'transfer', 300, False)
        exit(1)

    # 保存状态到CSV
    try:
        bank.save_state_to_csv('bank_state.csv')
    except Exception as e:
        print(f"Error saving state to CSV: {e}")
        exit(1)

    # 加载状态从CSV
    try:
        bank.load_state_from_csv('bank_state.csv')
    except Exception as e:
        print(f"Error loading state from CSV: {e}")
        exit(1)
