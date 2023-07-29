import mysql.connector as db


conn = db.connect(
    host = 'localhost',
    user = 'root',
    password = 'dts',
    database = 'dts',
)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS BankUsers (userId INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(25) UNIQUE, password VARCHAR(20))")
cur.execute("CREATE TABLE IF NOT EXISTS BankAccount (accountId INT PRIMARY KEY AUTO_INCREMENT, userId INT, username VARCHAR(25), balance INT)")
cur.execute("CREATE TABLE IF NOT EXISTS BankTransactions (transactionId INT PRIMARY KEY AUTO_INCREMENT, userId INT, withdrawed INT, deposited INT)")


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
            conn.commit()
            print("Sign-up successful!")
            break

def signIn():
    for i in range(3):
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        cur.execute(f"SELECT COUNT(*) FROM BankUsers WHERE username = '{username}' AND password = '{password}'")
        result = cur.fetchone()

        if result[0] > 0: # type: ignore
            print("Sign-in successful!")
            return
        else:
            print("Invalid username or password. Please try again.")

    print("Maximum sign-in attempts reached. Exiting...")