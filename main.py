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


# This class acts as a hub to controll all accounts and budgets
class FinanceTracker:
    def __init__(self):
        self._accounts = {}
        self._budgets = []

    def addAccount(self, account):
        self._accounts[account.getAccountName()] = account

    def addBudget(self, budget):
        self._budgets.append(budget)

    def getAccount(self, name):
        return self._accounts.get(name)

    def processTransaction(self, accountName, transaction):
        if accountName not in self._accounts:
            raise ValueError("Account not found")

        self._accounts[accountName].processTransaction(transaction)

    def getAllTransactions(self):
        allTx = []
        for account in self._accounts.values():
            allTx.extend(account.getTransactions())

        return allTx

    def generateReport(self):
        allTx = self.getAllTransactions()
        
        accountSummaries = []
        for name, account in self._accounts.items():
            accountSummaries.append({"name": name, "balance": account.getBalance()})

        budgetSummaries = []
        for budget in self._budgets:
            budgetSummaries.append(budget.getStatusReport(allTx))

        return {"accounts": accountSummaries, "budgets": budgetSummaries}


# CLI interface menu loop
def main():
    tracker = FinanceTracker()
    
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Create account")
        print("2. Set up budget")
        print("3. Log transaction")
        print("4. Print financial summary")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == "1":
            acc_type = input("Account type (checking/credit): ").strip().lower()
            name = input("Account name: ").strip()
            
            if acc_type == "checking":
                bal = float(input("Starting balance: "))
                tracker.addAccount(CheckingAccount(name, bal))
                print("Checking account created")

            elif acc_type == "credit":
                limit = float(input("Credit limit: "))
                tracker.addAccount(CreditCard(name, limit))
                print("Credit card created")
            else:
                print("Invalid account type")

        elif choice == "2":
            category = input("Category name: ").strip()
            limit = float(input("Spending limit: "))
            tracker.addBudget(Budget(category, limit))
            print("Budget created")

        elif choice == "3":
            tx_type = input("Transaction type (expense/income): ").strip().lower()
            acc_name = input("Account name: ").strip()
            amount = float(input("Amount: "))
            category = input("Category: ").strip()
            desc = input("Description: ").strip()

            try:
                if tx_type == "expense":
                    tx = Expense(amount, category, desc)

                elif tx_type == "income":
                    tx = Income(amount, category, desc)

                else:
                    print("Invalid transaction type")
                    continue

                tracker.processTransaction(acc_name, tx)
                print("Transaction processed")
            except Exception as e:
                print("Error processing transaction:", e)

        elif choice == "4":
            report = tracker.generateReport()
            print("\nAccounts")

            for acc in report["accounts"]:
                print(f"Name: {acc['name']} | Balance: ${acc['balance']:.2f}")

            print("\nBudgets")
            for b in report["budgets"]:
                print(f"Category: {b['category']} | Limit: ${b['limit']:.2f} | Spent: ${b['totalSpent']:.2f} | Status: {b['status']}")


        elif choice == "5":
            print("Goodbye")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
