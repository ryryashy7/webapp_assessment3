import hashlib
import os
import csv

accounts = []

# ------------------------
# Load accounts from CSV
# ------------------------
def accounts_load():
    try:
        with open("website/accounts.csv", "r") as ac:
            reader = csv.reader(ac)
            for row in reader:
                if len(row) == 3:
                    accounts.append({
                        "username": row[0],
                        "salt": row[1],
                        "password_hash": row[2]
                    })
    except FileNotFoundError:
        print("No accounts file found. Starting with an empty account list.")

accounts_load()

# ------------------------
# Register new account
# ------------------------
def register():
    username = input("Username: ")
    password = input("Password: ")

    salt = os.urandom(16)

    stored_hash = hashlib.scrypt(
        password.encode(),
        salt=salt,
        n=16384,
        r=8,
        p=1
    )

    with open("website/accounts.csv", "a", newline="") as ac:
        writer = csv.writer(ac)
        writer.writerow([username, salt.hex(), stored_hash.hex()])

    print("\n=== ACCOUNT CREATED ===")
    print(f"Username: {username}")
    print(f"Salt: {salt.hex()}")
    print(f"Hash: {stored_hash.hex()}\n")

    # FIXED: add new account to memory list
    accounts.append({
        "username": username,
        "salt": salt.hex(),
        "password_hash": stored_hash.hex()
    })

# ------------------------
# Login
# ------------------------
def login():
    print("=== LOGIN ===\n")

    entered_username = input("Enter username: ")
    entered_password = input("Enter password: ")

    # FIXED: search for matching account instead of using accounts[0]
    account = next((a for a in accounts if a["username"] == entered_username), None)

    if account is None:
        print("\nInvalid username")
        return

    # FIXED: convert stored hex salt back to bytes
    salt_bytes = bytes.fromhex(account["salt"])

    # FIXED: hash entered password using correct salt
    entered_hash = hashlib.scrypt(
        entered_password.encode(),
        salt=salt_bytes,
        n=16384,
        r=8,
        p=1
    ).hex()

    print("\n=== VERIFICATION PROCESS ===")
    print(f"Stored Salt:   {account['salt']}")
    print(f"Stored Hash:   {account['password_hash']}")
    print(f"Entered Hash:  {entered_hash}")

    # FIXED: compare entered hash to stored hash
    if entered_hash == account["password_hash"]:
        print("\nPassword correct!")
        print("Access granted.")
    else:
        print("\nPassword incorrect!")
        print("Access denied.")

# ------------------------
# Menu
# ------------------------
# FIXED: removed recursion and replaced with simple menu
choice = input("Do you want to login or register? (L/R) ").lower()

if choice == "r":
    register()
elif choice == "l":
    login()
else:
    print("Invalid option.")
