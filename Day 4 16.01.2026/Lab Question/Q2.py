# Topics: Parameterized Methods, Constructors & Destructors

# Create a class BankAccount that:

# 1. Uses a parameterized constructor to initialize account_number and balance

# 2. Implements methods deposit(amount) and withdraw(amount)

# 3. Uses a destructor to display a message when the object is deleted

# 4. Handle invalid withdrawal using proper checks


class BankAccount:
    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance
        print(f"Account {self.account_number} created with initial balance: ₹{self.balance}")
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"₹{amount} deposited successfully. New balance: ₹{self.balance}")
        else:
            print("Invalid deposit amount! Amount must be positive.")
    
    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid withdrawal amount! Amount must be positive.")
        elif amount > self.balance:
            print(f"Insufficient balance! Available balance: ₹{self.balance}")
        else:
            self.balance -= amount
            print(f"₹{amount} withdrawn successfully. Remaining balance: ₹{self.balance}")
    
    def __del__(self):
        print(f"Account {self.account_number} is being closed. Final balance: ₹{self.balance}")


print("=" * 50)
print("Banking Operations")
print("=" * 50)

account1 = BankAccount("ACC001", 5000)
print()

account1.deposit(2000)
account1.withdraw(1500)
account1.withdraw(10000)  
account1.withdraw(-500)   
print()

account2 = BankAccount("ACC002", 10000)
print()

account2.deposit(5000)
account2.withdraw(3000)
print()

print("=" * 50)
print("Program ending - accounts will be destroyed")
print("=" * 50)
