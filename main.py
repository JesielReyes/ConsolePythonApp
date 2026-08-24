import User

if __name__ == "__main__":
    users = {}
    while True:
        print("Welcome to the Banking System")
        print("1. Create User")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            pin = input("Enter a 4-digit PIN: ")
            if len(pin) != 4 or not pin.isdigit():
                print("Invalid PIN. Please enter a 4-digit PIN.")
                continue
            if pin in users:
                print("User with this PIN already exists. Please try again.")
                continue
            user = User.User(pin)
            print("User created successfully!")
            users[pin] = user
        elif choice == "2":
            if not users:
                print("No users found. Please create a user first.")
                continue
            pin = input("Enter your PIN: ")
            if pin in users and users[pin].check_pin(pin):
                user = users[pin]
                while True:
                    print("1. Create Account")
                    print("2. View Accounts")
                    print("3. Make Purchase")
                    print("4. Change PIN")
                    print("5. Logout")
                    choice = input("Enter your choice: ")
                    if choice == "1":
                        try:
                            account_type = input("Enter account type (Checking, Savings, Credit, Business, Investment): ")
                            print(f"Minimum balance: {user.get_minimum_balance(account_type)}")
                            balance = float(input("Enter initial balance: "))
                            account_number = user.create_account(pin, account_type, balance)
                            print(f"{account_type} account created successfully! Account Number: {account_number}")
                        except ValueError as e:
                            print(e)
                    elif choice == "2":
                        try:
                            user.get_all_accounts(pin)
                        except ValueError as e:
                            print(e)
                    elif choice == "3":
                        try:
                            account_type = input("Enter account type (Checking, Savings, Credit, Business, Investment): ")
                            user.can_make_purchase(pin, account_type)
                            print(f"Available accounts of type {account_type}: {', '.join([f'Account Number: {account.get_account_number()}, Balance: {account.get_balance()}' for account in user.get_accounts(pin, account_type).values()])}")
                            account_number = int(input("Enter account number: "))
                            amount = float(input("Enter purchase amount: "))
                            user.make_purchase(pin, account_type, account_number, amount)
                            print(f"Purchase of {amount} made successfully from {account_type} account {account_number}.")
                            print(f"New balance: {user.get_account(pin, account_type, account_number).get_balance()}")
                        except ValueError as e:
                            print(e)
                    elif choice == "4":
                        old_pin = input("Enter old PIN: ")
                        new_pin = input("Enter new PIN: ")
                        if len(new_pin) != 4 or not new_pin.isdigit():
                            print("Invalid new PIN. Please enter a 4-digit PIN.")
                            continue
                        try:
                            user.change_pin(old_pin, new_pin)
                        except ValueError as e:
                            print(e)
                    elif choice == "5":
                        break
                    else:
                        print("Invalid choice!")
            else:
                print("Invalid PIN!")
        elif choice == "3":
            break
        else:
            print("Invalid choice!")