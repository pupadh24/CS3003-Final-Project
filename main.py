from abc import ABC, abstractmethod
from datetime import datetime

# This is an abstract blueprint showing us our financial transactions and this is immutable
class Transaction(ABC):
    def __init__(self, amount, category, description):
        if type(self) is Transaction:
            raise TypeError("Transaction is an abstract class and cannot be instantiated directly")
        
        self._amount = amount
        self._category = category
        self._description = description
        self._timestamp = datetime.now()

    def getAmount(self):
        return self._amount

    def getCategory(self):
        return self._category

    def getDescription(self):
        return self._description

    def getTimestamp(self):
        return self._timestamp


# This is an abstract blueprint representing a financial account and this is encapsulated
class Account(ABC):
    def __init__(self, accountName, initialBalance = 0.0):
        if type(self) is Account:
            raise TypeError("Account is an abstract class and cannot be instantiated directly")
        
        self._accountName = accountName
        self._balance = initialBalance
        self._transactions = []

    def getAccountName(self):
        return self._accountName

    def getBalance(self):
        return self._balance

    def getTransactions(self):
        return list(self._transactions)

    def _updateBalance(self, amount):
        self._balance += amount

    @abstractmethod
    def processTransaction(self, transaction):
        pass


