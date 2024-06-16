import random

class Bank:
    def __init__(self):
        self.users = {}
        self.is_bankrupt = False
        self.total_loan_amount = 0

    def generate_account_number(self):
        return random.randint(10000, 99999)

    def is_bankrupt_check(func):
        def wrapper(*args, **kwargs):
            if args[0].bank.is_bankrupt:
                print("The bank is bankrupt. No transactions can be processed.")
                return
            return func(*args, **kwargs)
        return wrapper

class User:
    def __init__(self, name, email, address, account_type, bank):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.account_number = bank.generate_account_number()
        self.balance = 0
        self.transaction_history = []
        self.loan_count = 0
        self.bank = bank
        bank.users[self.account_number] = self

    @Bank.is_bankrupt_check
    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append(('Deposit', amount))
        print(f"{amount} deposited. New balance is {self.balance}.")

    @Bank.is_bankrupt_check
    def withdraw(self, amount):
        if amount > self.balance:
            print("Withdrawal amount exceeded.")
            return
        self.balance -= amount
        self.transaction_history.append(('Withdraw', amount))
        print(f"{amount} withdrawn. New balance is {self.balance}.")

    def check_balance(self):
        print(f"Available balance: {self.balance}")

    def check_transaction_history(self):
        for transaction in self.transaction_history:
            print(transaction)

    @Bank.is_bankrupt_check
    def take_loan(self, amount):
        if self.loan_count < 2:
            self.balance += amount
            self.bank.total_loan_amount += amount
            self.loan_count += 1
            self.transaction_history.append(('Loan', amount))
            print(f"Loan of {amount} approved.")
        else:
            print("Loan limit reached. Cannot take more loans.")

    @Bank.is_bankrupt_check
    def transfer(self, to_account_number, amount):
        if amount > self.balance:
            print("Insufficient funds for transfer.")
            return
        if to_account_number not in self.bank.users:
            print("Account does not exist.")
            return
        recipient = self.bank.users[to_account_number]
        recipient.balance += amount
        self.balance -= amount
        self.transaction_history.append(('Transfer', amount, to_account_number))
        print(f"Transferred {amount} to account {to_account_number}.")

class Admin:
    def __init__(self, bank):
        self.bank = bank

    def create_account(self, name, email, address, account_type):
        new_user = User(name, email, address, account_type, self.bank)
        print(f"Account created for {name} with account number {new_user.account_number}.")

    def delete_account(self, account_number):
        if account_number in self.bank.users:
            del self.bank.users[account_number]
            print(f"Account {account_number} deleted.")
        else:
            print("Account does not exist.")

    def list_accounts(self):
        if not self.bank.users:  
            print("No account is created")
        else:
            for account_number, user in self.bank.users.items():
                print(f"Account Number: {account_number}, Name: {user.name}, Balance: {user.balance}")

    def check_total_balance(self):
        total_balance = sum(user.balance for user in self.bank.users.values())
        print(f"Total available balance in the bank: {total_balance}")

    def check_total_loan_amount(self):
        print(f"Total loan amount: {self.bank.total_loan_amount}")

    def toggle_loan_feature(self):
        self.bank.is_bankrupt = not self.bank.is_bankrupt
        status = "on" if not self.bank.is_bankrupt else "off"
        print(f"Loan feature turned {status}.")

def user_menu(bank):
    while True:
        print("\nUser Menu:")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Check Transaction History")
        print("6. Take Loan")
        print("7. Transfer Amount")
        print("8. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            address = input("Enter your address: ")
            account_type = input("Enter account type (Savings/Current): ")
            user = User(name, email, address, account_type, bank)
            print(f"Account created successfully with account number: {user.account_number}")
        elif choice == '2':
            account_number = int(input("Enter your account number: "))
            amount = float(input("Enter amount to deposit: "))
            if account_number in bank.users:
                bank.users[account_number].deposit(amount)
            else:
                print("Account does not exist.")
        elif choice == '3':
            account_number = int(input("Enter your account number: "))
            amount = float(input("Enter amount to withdraw: "))
            if account_number in bank.users:
                bank.users[account_number].withdraw(amount)
            else:
                print("Account does not exist.")
        elif choice == '4':
            account_number = int(input("Enter your account number: "))
            if account_number in bank.users:
                bank.users[account_number].check_balance()
            else:
                print("Account does not exist.")
        elif choice == '5':
            account_number = int(input("Enter your account number: "))
            if account_number in bank.users:
                bank.users[account_number].check_transaction_history()
            else:
                print("Account does not exist.")
        elif choice == '6':
            account_number = int(input("Enter your account number: "))
            amount = float(input("Enter loan amount: "))
            if account_number in bank.users:
                bank.users[account_number].take_loan(amount)
            else:
                print("Account does not exist.")
        elif choice == '7':
            account_number = int(input("Enter your account number: "))
            recipient_account_number = int(input("Enter recipient's account number: "))
            amount = float(input("Enter amount to transfer: "))
            if account_number in bank.users and recipient_account_number in bank.users:
                bank.users[account_number].transfer(recipient_account_number, amount)
            else:
                print("One or both accounts do not exist.")
        elif choice == '8':
            break
        else:
            print("Invalid option. Please choose a valid option.")
        
def admin_login():
    admin_name = input("Enter admin name: ")
    admin_email = input("Enter admin email: ")
    admin_password = input("Enter admin password: ")
    if admin_name != "admin" or admin_email != "admin@bank.com" or admin_password != "1234":
        print("Admin credential is not Valid")
        return False
    return True

def admin_menu(admin):
    if not admin_login():
        return  

    while True:
        print("\nAdmin Menu:")
        print("1. Create Account")
        print("2. Delete Account")
        print("3. List All Accounts")
        print("4. Check Total Balance")
        print("5. Check Total Loan Amount")
        print("6. Toggle Loan Feature")
        print("7. Set Bank to Bankrupt")
        print("8. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Enter user's name: ")
            email = input("Enter user's email: ")
            address = input("Enter user's address: ")
            account_type = input("Enter account type (Savings/Current): ")
            admin.create_account(name, email, address, account_type)
        elif choice == '2':
            account_number = int(input("Enter the account number to delete: "))
            admin.delete_account(account_number)
        elif choice == '3':
            admin.list_accounts()
        elif choice == '4':
            admin.check_total_balance()
        elif choice == '5':
            admin.check_total_loan_amount()
        elif choice == '6':
            admin.toggle_loan_feature()
        elif choice == '7':
            admin.bank.is_bankrupt = True
            print("Bank status set to bankrupt. No further transactions can be processed.")
        elif choice == '8':
            break
        else:
            print("Invalid option. Please choose a valid option.")
        
def main():
    bank = Bank()
    admin = Admin(bank)

    while True:
        print("\nMain Menu:")
        print("1. User")
        print("2. Admin")
        print("3. Exit")
        role = input("Enter the number corresponding to your role: ").strip().lower()
        if role == '3' or role == 'exit':
            print("Exiting the system. Goodbye!")
            break
        elif role == '1' or role == 'user':
            user_menu(bank)
        elif role == '2' or role == 'admin':
            admin_menu(admin)
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
