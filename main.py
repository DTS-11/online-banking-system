import sys

import mysql.connector as db
import tabulate


conn = db.connect(
    host = 'localhost',
    user = 'root',
    password = 'dts',
    database = 'dts',
)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS BankUsers (userId INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(25) UNIQUE, password VARCHAR(20))")
cur.execute("CREATE TABLE IF NOT EXISTS BankAccount (accountId INT PRIMARY KEY AUTO_INCREMENT, userId INT, username VARCHAR(25), balance INT)")


def signUp():
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        cur.execute(f"SELECT COUNT(*) FROM BankUsers WHERE username = '{username}'")
        result = cur.fetchone()

        if result[0] > 0: # type: ignore
            print("Username is already taken. Please enter a new unique username.")

        else:
            cur.execute(f"INSERT INTO BankUsers (username, password) VALUES ('{username}', '{password}')")
            print("Sign-up successful!")
            conn.commit()

            cur.execute(f"SELECT userId FROM BankUsers WHERE username = '{username}'")
            user_id = cur.fetchone()[0]

            cur.execute(f"INSERT INTO BankAccount (userId, username, balance) VALUES ({user_id}, '{username}', 500)")
            conn.commit()

            print("As a head start, we've deposited 500 into your account!")
            print("Thank you for choosing Digital Bank Ltd.")

        break


def signIn():
    for i in range(3):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        print()

        cur.execute(f"SELECT COUNT(*) FROM BankUsers WHERE username = '{username}' AND password = '{password}'")
        result = cur.fetchone()

        if result[0] > 0: # type: ignore
            print("Sign-in successful!\n")
            return username
        
        else:
            print("Invalid username or password. Please try again.")

    print("\nMaximum sign-in attempts reached. Exiting...")
    sys.exit()


def balance(username):
    cur.execute(f"SELECT COUNT(*) FROM BankUsers WHERE username = '{username}'")
    result = cur.fetchone()

    if result[0] == 0:
        print("User not found.")
        return

    cur.execute(f"SELECT balance FROM BankAccount WHERE username = '{username}'")
    balance_result = cur.fetchone()

    if not balance_result:
        print("Error: Unable to retrieve account balance.")
        return

    balance = balance_result[0]

    data = [[username, balance]] # type: ignore
    headers = ["Username", "Balance"]
    table = tabulate.tabulate(data, headers=headers, tablefmt="pretty")

    print(table)

def withdraw(username):
    amount = int(input("Enter amount to withdraw: "))

    cur.execute(f"SELECT COUNT(*) FROM BankUsers WHERE username = '{username}'")
    result = cur.fetchone()

    if result[0] == 0:
        print("User not found. Please sign up first.")
        return

    cur.execute(f"SELECT balance FROM BankAccount WHERE username = '{username}'")
    balance = cur.fetchone()

    if not balance:
        print("Error: Unable to retrieve account balance.")
        return

    balance = balance[0]

    if amount > balance: # type: ignore
        print("Insufficient balance. Withdrawal not possible.")
    else:
        new_balance = balance - amount # type: ignore

        cur.execute(f"UPDATE BankAccount SET balance = {new_balance} WHERE username = '{username}'")
        conn.commit()

        print(f"Withdrawal successful. \nRemaining balance: {new_balance}")


def deposit(username):
    amount = int(input("Enter amount to deposit: "))

    cur.execute(f"SELECT COUNT(*) FROM BankUsers WHERE username = '{username}'")
    result = cur.fetchone()

    if result[0] == 0:
        print("User not found. Please sign up first.")
        return

    cur.execute(f"SELECT balance FROM BankAccount WHERE username = '{username}'")
    balance = cur.fetchone()

    if not balance:
        print("Error: Unable to retrieve account balance.")
        return

    balance = balance[0]

    new_balance = balance + amount # type: ignore

    cur.execute(f"UPDATE BankAccount SET balance = {new_balance} WHERE username = '{username}'")
    conn.commit()

    print(f"Deposit successful. \nNew balance: {new_balance}")


def send(recipient_username):
    sender_username = input("Enter username of the person you want to transfer: ")
    amount = int(input("Enter amount to transfer: "))

    cur.execute(f"SELECT COUNT(*) FROM BankUsers WHERE username = '{sender_username}'")
    sender_result = cur.fetchone()

    cur.execute(f"SELECT COUNT(*) FROM BankUsers WHERE username = '{recipient_username}'")
    recipient_result = cur.fetchone()

    if sender_result[0] == 0 or recipient_result[0] == 0:
        print("Invalid sender or recipient. Please check the username.")
        return

    cur.execute(f"SELECT balance FROM BankAccount WHERE username = '{sender_username}'")
    sender_balance = cur.fetchone()

    if not sender_balance:
        print("Error: Unable to retrieve sender's account balance.")
        return

    sender_balance = sender_balance[0]

    if amount > sender_balance: # type: ignore
        print("Insufficient balance. Sending money not possible.")
        return

    new_sender_balance = sender_balance - amount # type: ignore

    cur.execute(f"UPDATE BankAccount SET balance = {new_sender_balance} WHERE username = '{sender_username}'")

    cur.execute(f"SELECT balance FROM BankAccount WHERE username = '{recipient_username}'")
    recipient_balance = cur.fetchone()

    if not recipient_balance:
        print("Error: Unable to retrieve recipient's account balance.")
        return

    recipient_balance = recipient_balance[0]

    new_recipient_balance = recipient_balance + amount # type: ignore

    cur.execute(f"UPDATE BankAccount SET balance = {new_recipient_balance} WHERE username = '{recipient_username}'")

    conn.commit()

    print("Money sent successfully.")
    print(f"New sender's balance: {new_sender_balance}")
    print(f"New recipient's balance: {new_recipient_balance}")



print("=============================")
print("Welcome to Digital Bank Ltd.!")
print("=============================")
print()

res1 = input("What'd you like to do?\n1. Sign up\n2. Sign in\n\n")
user = ''

if res1 == '1':
    signUp()
    print("\nPlease login first.\n")
    user = signIn()

elif res1 == '2':
    user = signIn()


while True:
    print("\nWhat'd you like to do?")
    res2 = input("1. View Balance\n2. Withdraw\n3. Deposit\n4. Send Money\n5. Quit\n\n")


    if res2 == '1':
        balance(user)

    elif res2 == '2':
        withdraw(user)

    elif res2 == '3':
        deposit(user)

    elif res2 == '4':
        send(user)

    elif res2 == '5':
        print("Terminating the process...")
        sys.exit()
    
    else:
        print("Invalid choice")