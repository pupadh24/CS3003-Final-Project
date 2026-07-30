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

class Expense(Transaction):
    pass

class Income(Transaction):
    pass


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

    @abstractmethod
    def processTransaction(self, transaction):
        pass

class CheckingAccount(Account):
    def processTransaction(self, transaction):
        if isinstance(transaction, Expense):
            if self.getBalance() - transaction.getAmount() < 0:
                raise ValueError("Your transaction has been blocked")
            self._balance -= transaction.getAmount()
            self._transactions.append(transaction)
            
        elif isinstance(transaction, Income):
            self._balance += transaction.getAmount()
            self._transactions.append(transaction)
        else:
            raise TypeError("Invalid transaction type")


class CreditCard(Account):
    def __init__(self, accountName, creditLimit, initialBalance = 0.0):
        super().__init__(accountName, initialBalance)
        self._creditLimit = creditLimit

    def getCreditLimit(self):
        return self._creditLimit

    def processTransaction(self, transaction):
        if isinstance(transaction, Expense):
            if self.getBalance() + transaction.getAmount() > self._creditLimit:
                raise ValueError("Your transaction has been blocked")
            self._balance += transaction.getAmount()
            self._transactions.append(transaction)

        elif isinstance(transaction, Income):
            self._balance -= transaction.getAmount()
            self._transactions.append(transaction)

        else:
            raise TypeError("Invalid transaction type")


# This class tracks spending limits for a specific category
class Budget:
    def __init__(self, category, limit):
        self._category = category
        self._limit = limit

    def getCategory(self):
        return self._category

    def getLimit(self):
        return self._limit

    def calculateTotalSpent(self, transactions):
        total = 0.0
        for t in transactions:
            if isinstance(t, Expense) and t.getCategory().lower() == self._category.lower():
                total += t.getAmount()
        return total

    def getStatusReport(self, transactions):
        spent = self.calculateTotalSpent(transactions)
        remaining = self._limit - spent
        isOverBudget = spent > self._limit
        
        if isOverBudget:
            warning = "Warning: over budget"
        else:
            warning = "Within budget"

        return {
            "category": self._category,
            "limit": self._limit,
            "totalSpent": spent,
            "remaining": remaining,
            "isOverBudget": isOverBudget,
            "status": warning
        }

