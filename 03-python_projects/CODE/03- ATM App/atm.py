def welcome():
    print('Welcome to the Simple ATM!')

def main_menu():
    print('''
    1. Deposit Money
    2. Withdraw Money
    3. Check Balance
    4. Exit
    ''')

def deposit_money():
    amount = float(input('Enter the amount to deposit: '))
    global balance
    balance += amount
    print(f'You have successfully deposited ${amount}')

def withdraw_money():
    amount = float(input('Enter the amount to withdraw: '))
    global balance
    if amount > balance:
        print('Insufficient balance!')
        return
    else:
        balance -= amount
        print(f'You have successfully withdrawn ${amount}')

def check_balance():
    global balance
    print(f'Your current balance is ${balance}')

def atm():
    global balance
    balance = 0
    welcome()
    while True:
        main_menu()
        choice = int(input('Enter your choice: '))
        if choice == 1:
            deposit_money()
        elif choice == 2:
            withdraw_money()
        elif choice == 3:
            check_balance()
        elif choice == 4:
            print('Goodbye!')
            break
        else:
            print('Invalid choice!')

if __name__ == '__main__':
    atm()

